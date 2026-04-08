import re
import json
import base64
import os
from PIL import Image
from image_utils import smart_crop, img_to_b64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, '2025A_IP_Questions_OCR.txt')
ANSWERS_FILE = os.path.join(BASE_DIR, '2025A_IP_Answers_OCR.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'questions_51_100.jsonl')
PAGES_DIR = os.path.join(BASE_DIR, 'pages')

tag_map = {
    "#BasicTheory": "7. Basic Theory", 
    "#ComputerSystems": "8. Computer System",
    "#TechnicalElements": "9. Technology Element", 
    "#DevelopmentTechniques": "4. Development Strategy",
    "#ProjectManagement": "5. Project Management", 
    "#ServiceManagement": "6. Service Management",
    "#SystemStrategy": "3. System Strategy", 
    "#CorporateLegalAffairs": "1. Corporate and legal affairs",
    "#ManagementStrategy": "2. Business Strategy",
    "#SystemAudit": "6. Service Management",
    "#Unknown": "10. Other (Categorization Pending)"
}

categories = {
    "Q51": "#ProjectManagement",
    "Q52": "#ProjectManagement",
    "Q53": "#ProjectManagement",
    "Q54": "#ProjectManagement",
    "Q55": "#ProjectManagement",
    "Q56": "#BasicTheory",
    "Q57": "#ProjectManagement",
    "Q58": "#ServiceManagement",
    "Q59": "#ServiceManagement",
    "Q60": "#ServiceManagement",
    "Q61": "#ServiceManagement",
    "Q62": "#ServiceManagement",
    "Q63": "#SystemAudit",
    "Q64": "#SystemStrategy",
    "Q65": "#CorporateLegalAffairs",
    "Q66": "#BasicTheory",
    "Q67": "#CorporateLegalAffairs",
    "Q68": "#ManagementStrategy",
    "Q69": "#ManagementStrategy",
    "Q70": "#ManagementStrategy",
    "Q71": "#CorporateLegalAffairs",
    "Q72": "#CorporateLegalAffairs",
    "Q73": "#CorporateLegalAffairs",
    "Q74": "#CorporateLegalAffairs",
    "Q75": "#TechnicalElements",
    "Q76": "#TechnicalElements",
    "Q77": "#CorporateLegalAffairs",
    "Q78": "#CorporateLegalAffairs",
    "Q79": "#ManagementStrategy",
    "Q80": "#ManagementStrategy",
    "Q81": "#ManagementStrategy",
    "Q82": "#ManagementStrategy",
    "Q83": "#ManagementStrategy",
    "Q84": "#ManagementStrategy",
    "Q85": "#ManagementStrategy",
    "Q86": "#ManagementStrategy",
    "Q87": "#ManagementStrategy",
    "Q88": "#TechnicalElements",
    "Q89": "#ManagementStrategy",
    "Q90": "#BasicTheory",
    "Q91": "#ManagementStrategy",
    "Q92": "#ManagementStrategy",
    "Q93": "#ComputerSystems",
    "Q94": "#TechnicalElements",
    "Q95": "#TechnicalElements",
    "Q96": "#SystemStrategy",
    "Q97": "#SystemStrategy",
    "Q98": "#DevelopmentTechniques",
    "Q99": "#SystemStrategy",
    "Q100": "#ManagementStrategy"
}

def parse_all():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip Page 1 and Page 2 (Cover and Disclaimers)
    page3_marker = "--- Page 3 ---"
    if page3_marker in content:
        content = content[content.find(page3_marker):]
    
    # Handle math symbols
    content = content.replace('', '∪').replace('', '∩')
    
    # Locate page markers
    page_markers = []
    for m in re.finditer(r'--- Page (\d+) ---', content):
        page_markers.append((m.start(), int(m.group(1))))
    
    # Extract questions
    questions = {}
    q_matches = list(re.finditer(r'(?:^|\n)(Q\d+)\.', content))
    
    for i in range(len(q_matches)):
        m = q_matches[i]
        q_id = m.group(1)
        q_num = int(q_id[1:])
        if q_num < 51: continue
        
        start_pos = m.end()
        end_pos = q_matches[i+1].start() if i+1 < len(q_matches) else len(content)
        
        q_block = content[start_pos:end_pos]
        
        # Determine page
        q_page = 1
        for p_pos, p_num in page_markers:
            if p_pos <= m.start(): q_page = p_num
            else: break
        
        # Split into question text and choices
        # Look for a), b), c), d)
        choices = {"a": "", "b": "", "c": "", "d": ""}
        
        parts = re.split(r'\n\s*([a-d])\)', q_block)
        # parts[0] is question text
        # parts[1] is 'a', parts[2] is choice 'a' content, etc.
        
        q_text = parts[0].strip()
        for j in range(1, len(parts), 2):
            letter = parts[j]
            content_part = parts[j+1].strip()
            choices[letter] = content_part
            
        # Clean up question text and choices
        def clean(t):
            t = re.sub(r'--- Page \d+ ---', '', t)
            t = re.sub(r'– \d+ –', '', t)
            return t.strip()
        
        q_text = clean(q_text)
        for k in choices:
            choices[k] = clean(choices[k])
            
        # Check for media
        keywords = ['diagram', 'figure', 'table', 'below', 'figure below']
        has_media = any(kw.lower() in q_text.lower() for kw in keywords) or \
                    any(any(kw.lower() in choices[k].lower() for kw in keywords) for k in choices)

        questions[q_id] = {
            "question_text": q_text,
            "choices": choices,
            "has_media": has_media,
            "page": q_page
        }

    # Answers
    answers = {}
    with open(ANSWERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.search(r'(Q\d+)\s+([a-d])', line)
            if m:
                answers[m.group(1)] = m.group(2)
                
    return questions, answers

def main():
    questions, answers = parse_all()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for i in range(51, 101):
            q_id = f"Q{i}"
            if q_id not in questions: continue
            
            q_data = questions[q_id]
            tag = categories.get(q_id, "#Unknown")
            media = []
            
            if q_data["has_media"]:
                img_path = os.path.join(PAGES_DIR, f"page-{q_data['page']:02d}.jpg")
                if os.path.exists(img_path):
                    with Image.open(img_path) as img:
                        cropped = smart_crop(img, f"2025A-{q_id}")
                        b64 = img_to_b64(cropped)
                        media.append({
                            "type": "image", 
                            "label": f"Diagram for {q_id}",
                            "base64": f"data:image/png;base64,{b64}"
                        })
            
            ans = answers.get(q_id, "")
            choice_text = q_data["choices"].get(ans, "")
            
            q_num_int = int(q_id[1:])
            json.dump({
                "id": f"2025A-Q-{q_num_int:03d}",
                "metadata": {
                    "topic": tag.replace("#", ""),
                    "major_category": tag_map.get(tag, "Unknown"),
                    "source": "IT Passport Oct 2025",
                    "page": q_data["page"]
                },
                "content": {
                    "question_text": q_data["question_text"],
                    "choices": q_data["choices"],
                    "has_media": q_data["has_media"],
                    "media": media
                },
                "feedback": { 
                    "correct_answer": ans,
                    "explanation": f"The correct answer for {q_id} is: {choice_text}."
                }
            }, f, ensure_ascii=False)
            f.write('\n')

if __name__ == "__main__":
    main()
