import json
import os
import re
from PIL import Image
from image_utils import img_to_b64

JSON_PATH = "opendataloader_test/2025A_IP_Questions.json"
ANSWERS_PATH = "2025A_IP_Answers_OCR.txt"
PDF_PAGES_DIR = "pages"
OUTPUT_FILE = "2025A_IP_Questions.jsonl"

def get_answers():
    answers = {}
    if not os.path.exists(ANSWERS_PATH): return answers
    with open(ANSWERS_PATH, 'r') as f:
        for line in f:
            m = re.match(r'Q(\d+)\s+([a-d])', line)
            if m: answers[int(m.group(1))] = m.group(2)
    return answers

def flatten_json(items, result=None):
    if result is None: result = []
    if isinstance(items, dict):
        result.append(items)
        for key in ["kids", "list items", "rows", "cells"]:
            if key in items: flatten_json(items[key], result)
    elif isinstance(items, list):
        for i in items: flatten_json(i, result)
    return result

def get_union_bbox(items, y_limit=None):
    if not items: return None
    # Filter for items with valid boxes
    # If y_limit is provided, ignore items whose top is above this limit
    valid_items = [it for it in items if "bounding box" in it and len(it.get("bounding box", [])) == 4]
    
    if y_limit is not None:
        # PDF coords: top is higher value. If item top > y_limit, it is physically ABOVE the limit.
        valid_items = [it for it in valid_items if it["bounding box"][1] < y_limit]

    if not valid_items: return None
    
    lefts = [it["bounding box"][0] for it in valid_items]
    bottoms = [it["bounding box"][1] for it in valid_items]
    rights = [it["bounding box"][2] for it in valid_items]
    tops = [it["bounding box"][3] for it in valid_items]
    return [min(lefts), min(bottoms), max(rights), max(tops)]

def main():
    if not os.path.exists(JSON_PATH): return
    with open(JSON_PATH, 'r') as f: data = json.load(f)
    all_answers = get_answers()
    
    # 1. Flatten the entire document
    flat_items = flatten_json(data["kids"])
    
    # 2. Identify Question Start Indices (Skipping Page 1/2)
    q_indices = []
    for i, item in enumerate(flat_items):
        content = str(item.get("content", ""))
        if re.match(r"^Q\d+\.", content) and item.get("page number", 0) >= 3:
            q_indices.append(i)
            
    final_questions = []
    for idx, start_idx in enumerate(q_indices):
        end_idx = q_indices[idx+1] if idx+1 < len(q_indices) else len(flat_items)
        
        # Everything between this Q and the next is part of this question
        # Refinement: Explicitly exclude footer elements to avoid page numbers in crops
        block_items = [it for it in flat_items[start_idx:end_idx] if it.get("type") != "footer"]
        
        # Get Q number and ID
        q_item = flat_items[start_idx]
        q_num = int(re.match(r"^Q(\d+)\.", q_item["content"]).group(1))
        q_id = f"2025A-Q-{q_num:03d}"
        page = q_item["page number"]
        
        # The absolute top of our search is the top of the Q marker itself
        q_start_top = q_item["bounding box"][3] if "bounding box" in q_item else 9999
        
        # 3. Identify Split Point (First Choice)
        split_y = None
        choice_items = []
        question_items = []
        found_choices = False
        
        for it in block_items:
            content = it.get("content", "")
            is_c = re.match(r'^\s*[a-d][\)\.]', content)
            
            if is_c:
                found_choices = True
                if "bounding box" in it:
                    y_top = it["bounding box"][3]
                    if split_y is None or y_top > split_y:
                        split_y = y_top
            
            if found_choices:
                choice_items.append(it)
            else:
                question_items.append(it)

        # 4. Calculate Bboxes (Prevent going above q_start_top)
        q_union = get_union_bbox(question_items, y_limit=q_start_top + 10)
        c_union = get_union_bbox(choice_items, y_limit=split_y + 10 if split_y else None)
        
        media = []
        img_path = os.path.join(PDF_PAGES_DIR, f"page-{page:02d}.jpg")
        
        if os.path.exists(img_path):
            with Image.open(img_path) as img:
                w, h = img.size
                scale_x, scale_y = w / 595.0, h / 842.0
                
                # Question Part
                if q_union:
                    # Use full width for diagrams
                    y1 = (842 - q_union[3]) * scale_y
                    y2 = (842 - (split_y if split_y else q_union[1])) * scale_y
                    crop_q = img.crop((0, max(0, y1-15), w, min(h, y2+5)))
                    media.append({"type": "image", "label": "Question", "base64": f"data:image/png;base64,{img_to_b64(crop_q)}"})
                
                # Choice Part
                if c_union and split_y:
                    y1_c = (842 - split_y) * scale_y
                    # Refinement: Use c_union[1] (the bottom of the choices) instead of block_bottom
                    # to strictly avoid page numbers.
                    y2_c = (842 - c_union[1]) * scale_y
                    
                    # Safety: Never crop below 95% of the page height (page numbers are usually at 97%+)
                    max_safe_y = h * 0.95
                    y2_c = min(y2_c + 15, max_safe_y)
                    
                    crop_c = img.crop((0, max(0, y1_c-5), w, y2_c))
                    media.append({"type": "image", "label": "Choices", "base64": f"data:image/png;base64,{img_to_b64(crop_c)}"})

        ans = all_answers.get(q_num, "a")
        final_questions.append({
            "id": q_id,
            "metadata": {"topic": "General", "major_category": "10. Other (Categorization Pending)", "source": "IT Passport Oct 2025", "page": page},
            "content": {
                "question_text": "", 
                "choices": {"a": "See Diagram (A)", "b": "See Diagram (B)", "c": "See Diagram (C)", "d": "See Diagram (D)"},
                "has_media": True,
                "media": media
            },
            "feedback": {
                "correct_answer": ans,
                "explanation": f"### Rationale\nThe correct answer is **({ans.upper()})** as shown in the original exam layout."
            }
        })

    final_questions.sort(key=lambda x: x["id"])
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for q in final_questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f"Marker-to-Marker Mode: Generated {len(final_questions)} questions in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
