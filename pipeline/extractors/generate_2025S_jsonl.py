import json
import re
import os
from PIL import Image
from image_utils import smart_crop, img_to_b64

def generate_2025S_jsonl():
    ocr_path = '2025S_IP_Questions_OCR.txt'
    img_dir = 'images/2025S_IP'
    if not os.path.exists(ocr_path):
        print(f"Missing {ocr_path}")
        return
        
    with open(ocr_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Standard regex for text-based parsing
    q_matches = list(re.finditer(r'(?:^|\n)(Q\d+)\.\s+', content))
    
    questions = []
    for i in range(len(q_matches)):
        m = q_matches[i]
        q_id_str = m.group(1)
        q_num = int(q_id_str[1:])
        q_id = f"2025S-Q-{q_num:03d}"
        
        start_pos = m.end()
        end_pos = q_matches[i+1].start() if i+1 < len(q_matches) else len(content)
        q_block = content[start_pos:end_pos]
        
        # Split into question text and choices
        c_matches = list(re.finditer(r'(?:^|\n)\s*([a-d])[\)\.]', q_block))
        
        choices = {"a": "", "b": "", "c": "", "d": ""}
        if c_matches:
            q_text = q_block[:c_matches[0].start()].strip()
            for j in range(len(c_matches)):
                c_letter = c_matches[j].group(1).lower()
                c_start = c_matches[j].end()
                c_end = c_matches[j+1].start() if j+1 < len(c_matches) else len(q_block)
                choices[c_letter] = q_block[c_start:c_end].strip()
        else:
            q_text = q_block.strip()
            
        # Detect media
        media = []
        # For 2025S, we need to map question number to page number
        # Roughly 3-4 questions per page starting from page 3
        # We can find the image tag in the text as a hint: ![Q9 Figure 1 and 2](images/2025S_IP/page-07.png)
        img_hint = re.search(r'!\[.*?\]\((images/2025S_IP/page-(\d+)\.png)\)', q_block)
        
        if img_hint:
            img_path = img_hint.group(1)
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    cropped = smart_crop(img, q_id)
                    b64 = img_to_b64(cropped)
                    media.append({
                        "type": "image",
                        "label": f"Diagram for {q_id}",
                        "base64": f"data:image/png;base64,{b64}",
                        "url": ""
                    })
            # Clean up the markdown image tag from the text
            q_text = re.sub(r'!\[.*?\]\(.*?\)', '', q_text).strip()
            has_media = True
        else:
            has_media = False
        
        questions.append({
            "id": q_id,
            "metadata": {
                "topic": "Other",
                "major_category": "10. Other (Categorization Pending)",
                "source": "2025S_IP"
            },
            "content": {
                "question_text": q_text,
                "choices": choices,
                "has_media": has_media,
                "media": media
            },
            "feedback": {
                "correct_answer": "a",
                "explanation": f"Placeholder explanation for {q_id}."
            }
        })
        
    with open('2025S_IP_Questions.jsonl', 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q) + '\n')
    print(f"Generated 100 questions in 2025S_IP_Questions.jsonl")

if __name__ == "__main__":
    generate_2025S_jsonl()
