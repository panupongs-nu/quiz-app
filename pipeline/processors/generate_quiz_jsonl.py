import re
import json
import base64
import os
from PIL import Image
from image_utils import smart_crop, img_to_b64

# Base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, '2025A_IP_Questions_OCR.txt')
ANSWERS_FILE = os.path.join(BASE_DIR, '2025A_IP_Answers_OCR.txt')
CATEGORIZED_FILE = os.path.join(BASE_DIR, '2025A_IP_Categorized.md')
OUTPUT_FILE = os.path.join(BASE_DIR, '2025A_IP_Questions.jsonl')
PAGES_DIR = os.path.join(BASE_DIR, 'pages')

def parse_questions(file_path):
    """Extracts questions and choices, tracking page numbers via offsets."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip Page 1 and Page 2 (Cover and Disclaimers)
    page3_marker = "--- Page 3 ---"
    if page3_marker in content:
        content = content[content.find(page3_marker):]

    # Pre-process content: handle math symbols ( -> ∪,  -> ∩)
    content = content.replace('', '∪').replace('', '∩')

    # Locate page markers
    page_markers = []
    for m in re.finditer(r'--- Page (\d+) ---', content):
        page_markers.append((m.start(), int(m.group(1))))
    
    # Find all question starts and choice markers
    q_matches = list(re.finditer(r'(?:^|\n)(Q\d+)\.\s+', content))
    c_matches = list(re.finditer(r'(?:^|\n)\s*([a-d])[\)\.]', content))
    
    all_markers = []
    for m in q_matches:
        all_markers.append({'type': 'Q', 'id': m.group(1), 'pos': m.start(), 'end': m.end()})
    for m in c_matches:
        all_markers.append({'type': 'C', 'letter': m.group(1).lower(), 'pos': m.start(), 'end': m.end()})
    
    all_markers.sort(key=lambda x: x['pos'])

    questions = {}
    last_q_id = None
    
    for idx, m in enumerate(all_markers):
        next_marker_pos = all_markers[idx+1]['pos'] if idx + 1 < len(all_markers) else len(content)
        # Extract text and clean it
        raw_text = content[m['end']:next_marker_pos]
        raw_text = re.sub(r'--- Page \d+ ---', '', raw_text)
        raw_text = re.sub(r'\n\s*– \d+ –\s*\n', '\n', raw_text)
        
        if m['type'] == 'Q':
            q_id = m['id']
            # Determine page
            q_page = 1
            for p_pos, p_num in page_markers:
                if p_pos <= m['pos']: q_page = p_num
                else: break
            
            questions[q_id] = {
                "question_text": raw_text.strip(),
                "choices": {"a": "N/A", "b": "N/A", "c": "N/A", "d": "N/A"},
                "has_media": False,
                "page": q_page,
                "raw_block": "" 
            }
            last_q_id = q_id
        elif m['type'] == 'C':
            target_q_id = last_q_id
            letter = m['letter']
            
            # Heuristic for interleaved choices:
            # If current question has no 'a' yet, but we see 'b', 'c', or 'd', 
            # they likely belong to the previous question.
            if target_q_id:
                q_num = int(target_q_id[1:])
                prev_q_id = f"Q{q_num - 1}"
                if letter in ['b', 'c', 'd'] and questions[target_q_id]["choices"]["a"] == "N/A" and prev_q_id in questions:
                    target_q_id = prev_q_id
            
            if target_q_id:
                # If target_q_id is NOT the current question, the text might contain current Q's text
                if target_q_id != last_q_id and idx + 1 < len(all_markers) and all_markers[idx+1]['type'] == 'C' and all_markers[idx+1]['letter'] == 'a':
                    # Split heuristic: split by the FIRST double newline if it exists
                    if "\n\n" in raw_text:
                        parts = raw_text.split("\n\n", 1)
                        choice_content = parts[0]
                        q_content = parts[1]
                    elif "?" in raw_text:
                        parts = raw_text.split("?", 1)
                        choice_content = parts[0] + "?"
                        q_content = parts[1]
                    else:
                        choice_content = raw_text
                        q_content = ""
                    
                    questions[target_q_id]["choices"][letter] = choice_content.strip()
                    # Add orphaned q_content to the current question prefix
                    questions[last_q_id]["question_text"] = (q_content.strip() + "\n\n" + questions[last_q_id]["question_text"]).strip()
                else:
                    questions[target_q_id]["choices"][letter] = raw_text.strip()
                
                questions[target_q_id]["raw_block"] += " " + questions[target_q_id]["choices"][letter]
    
    # Final pass for cleanup and redistribution
    q_ids = sorted(questions.keys(), key=lambda x: int(x[1:]))
    for i in range(len(q_ids)):
        q = questions[q_ids[i]]
        # Standardize question_text
        q["question_text"] = q["question_text"].strip()
        # Standardize choices
        for k in q["choices"]:
            q["choices"][k] = q["choices"][k].strip()
            
        # If prev question has empty choices, look into current question text
        if i > 0:
            prev_q = questions[q_ids[i-1]]
            if all(prev_q["choices"][l] == "N/A" or not prev_q["choices"][l] for l in "abcd"):
                # Move prefix of current question text to prev question's choices
                if "\n\n" in q["question_text"] or "Which of the following" in q["question_text"]:
                    # Split by paragraph
                    parts = q["question_text"].split("Which of the following", 1)
                    if len(parts) > 1:
                        prev_q["choices"]["d"] = parts[0].strip()
                        q["question_text"] = ("Which of the following" + parts[1]).strip()

    # Final pass for media detection
    keywords = ['diagram', 'figure', 'table', 'below', 'figure below']
    for q_id in questions:
        q = questions[q_id]
        if any(kw.lower() in q["question_text"].lower() for kw in keywords) or \
           any(kw.lower() in q["raw_block"].lower() for kw in keywords):
            q["has_media"] = True
            
    return questions

def parse_metadata():
    """Parses correct answers and category tags from supporting files."""
    answers, categories = {}, {}
    if os.path.exists(ANSWERS_FILE):
        with open(ANSWERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.search(r'(Q\d+)\s+([a-d])', line)
                if m: answers[m.group(1)] = m.group(2)
    
    if os.path.exists(CATEGORIZED_FILE):
        with open(CATEGORIZED_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split by question number blocks
            blocks = re.split(r'- Question Number: (\d+)', content)
            for i in range(1, len(blocks), 2):
                q_num = f"Q{blocks[i]}"
                body = blocks[i+1]
                tag_match = re.search(r'- Category Tag: (#\w+)', body)
                if tag_match:
                    categories[q_num] = tag_match.group(1)
    return answers, categories

def main():
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
        "#Unknown": "10. Other (Categorization Pending)"
    }

    questions = parse_questions(QUESTIONS_FILE)
    answers, categories = parse_metadata()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for i in range(1, 101):
            q_key = f"Q{i}"
            if q_key not in questions: continue
            
            q_data = questions[q_key]
            tag = categories.get(q_key, "#Unknown")
            media = []
            
            if q_data["has_media"]:
                img_path = os.path.join(PAGES_DIR, f"page-{q_data['page']:02d}.jpg")
                if os.path.exists(img_path):
                    with Image.open(img_path) as img:
                        cropped = smart_crop(img, f"2025A-{q_key}")
                        b64 = img_to_b64(cropped)
                        media.append({
                            "type": "image", 
                            "label": f"Diagram for {q_key}",
                            "base64": f"data:image/png;base64,{b64}"
                        })
            
            q_num_int = int(q_key[1:])
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
                    "correct_answer": answers.get(q_key, ""),
                    "explanation": f"The correct answer for {q_key} is: {q_data['choices'].get(answers.get(q_key, ''), '')}."
                }
            }, f, ensure_ascii=False)
            f.write('\n')

if __name__ == "__main__":
    main()
