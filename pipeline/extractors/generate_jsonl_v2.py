import json
import os
import re
import sys
import argparse
from PIL import Image
from io import BytesIO
import base64

# Add pipeline/utils to sys.path to import image_utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
try:
    from image_utils import img_to_b64
except ImportError:
    # Fallback if pathing is weird
    def img_to_b64(img, format="PNG"):
        from io import BytesIO
        import base64
        buffered = BytesIO()
        img.save(buffered, format=format)
        return base64.b64encode(buffered.getvalue()).decode()

def get_answers(answers_path):
    answers = {}
    if not os.path.exists(answers_path):
        print(f"Warning: Answers file {answers_path} not found.")
        return answers
    with open(answers_path, 'r') as f:
        for line in f:
            m = re.match(r'Q(\d+)\s+([a-d])', line, re.IGNORECASE)
            if m:
                answers[int(m.group(1))] = m.group(2).lower()
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

def main():
    parser = argparse.ArgumentParser(description="Generate JSONL from OpenDataLoader JSON and PDF pages.")
    parser.add_argument("--year", required=True, help="Exam identifier (e.g., 2025S)")
    parser.add_argument("--json", required=True, help="Path to OpenDataLoader JSON output")
    parser.add_argument("--answers", required=True, help="Path to cleaned answers text file")
    parser.add_argument("--pages_dir", required=True, help="Directory containing page-XX.jpg images")
    parser.add_argument("--output", required=True, help="Path to save the output JSONL file")
    parser.add_argument("--source_name", default=None, help="Formal source name for metadata")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.json):
        print(f"Error: JSON file {args.json} not found.")
        return
    
    with open(args.json, 'r') as f:
        data = json.load(f)
    
    all_answers = get_answers(args.answers)
    source_label = args.source_name or f"IT Passport {args.year}"
    
    # 1. Flatten the entire document
    flat_items = flatten_json(data["kids"])
    
    # 2. Identify Question Start Indices (Skipping Page 1/2)
    q_indices = []
    for i, item in enumerate(flat_items):
        content = str(item.get("content", ""))
        # Match Q1. Q2. etc.
        if re.match(r"^Q\d+\.", content) and item.get("page number", 0) >= 3:
            q_indices.append(i)
            
    final_questions = []
    print(f"Found {len(q_indices)} questions in {args.year}")
    
    for idx, start_idx in enumerate(q_indices):
        end_idx = q_indices[idx+1] if idx+1 < len(q_indices) else len(flat_items)
        
        # Everything between this Q and the next is part of this question
        block_items = [it for it in flat_items[start_idx:end_idx] if it.get("type") != "footer"]
        
        # Get Q number and ID
        q_item = flat_items[start_idx]
        q_match = re.match(r"^Q(\d+)\.", q_item["content"])
        if not q_match: continue
        
        q_num = int(q_match.group(1))
        q_id = f"{args.year}-Q-{q_num:03d}"
        page_num = q_item["page number"]
        
        # Load the page image
        page_img_path = os.path.join(args.pages_dir, f"page-{page_num:02d}.jpg")
        if not os.path.exists(page_img_path):
            print(f"Warning: Page image {page_img_path} not found for {q_id}")
            continue
            
        page_img = Image.open(page_img_path)
        p_w, p_h = page_img.size
        
        # Identify Split Point (First Choice marker a) b) c) d) )
        split_y = None
        choice_items = []
        found_choices = False
        
        for it in block_items:
            content = it.get("content", "")
            is_c = re.match(r'^\s*[a-d][\)\.]', content)
            
            if is_c:
                found_choices = True
                if "bounding box" in it:
                    y_top = it["bounding box"][3] # top coord in PDF
                    if split_y is None or y_top > split_y:
                        split_y = y_top
            
            if found_choices:
                choice_items.append(it)
        
        # Calculate Bounding Boxes in PDF coordinates
        def get_bbox(items):
            valid = [it for it in items if "bounding box" in it and len(it["bounding box"]) == 4]
            if not valid: return None
            return [
                min(it["bounding box"][0] for it in valid),
                min(it["bounding box"][1] for it in valid),
                max(it["bounding box"][2] for it in valid),
                max(it["bounding box"][3] for it in valid)
            ]
            
        q_bbox_pdf = get_bbox([it for it in block_items if it not in choice_items])
        c_bbox_pdf = get_bbox(choice_items)
        
        # PDF box is [L, B, R, T] where (0,0) is bottom-left. 
        # Image box is [L, T, R, B] where (0,0) is top-left.
        # OpenDataLoader PDF height is usually 841.89 (A4) or 792 (Letter)
        # We need the page height in PDF units to flip Y
        # We'll assume the bounding box of the page or just use the max T found.
        # Actually, let's use a safer relative mapping.
        
        # Determine PDF page height from content if not explicitly in JSON
        # Usually it's in data["kids"] if we look for page type
        pdf_h = 841.89 # Default A4
        for it in flat_items:
            if "bounding box" in it:
                pdf_h = max(pdf_h, it["bounding box"][3])
        
        def pdf_to_img_box(pdf_box):
            if not pdf_box: return None
            l, b, r, t = pdf_box
            # Flip Y: img_top = (pdf_h - pdf_top) * scale
            # We need to calculate scale based on actual image pixels
            scale_x = p_w / 595.27 # PDF width A4
            scale_y = p_h / pdf_h
            
            # Use found content bounds for scale_x if 595.27 is wrong
            # But ITPE is usually A4.
            
            return [
                int(l * scale_x) - 10,
                int((pdf_h - t) * scale_y) - 10,
                int(r * scale_x) + 10,
                int((pdf_h - b) * scale_y) + 10
            ]
            
        q_img_box = pdf_to_img_box(q_bbox_pdf)
        c_img_box = pdf_to_img_box(c_bbox_pdf)
        
        media = []
        if q_img_box:
            # Clamp to image size
            q_img_box = [max(0, q_img_box[0]), max(0, q_img_box[1]), min(p_w, q_img_box[2]), min(p_h, q_img_box[3])]
            q_crop = page_img.crop(q_img_box)
            media.append({
                "type": "image",
                "label": "Question",
                "base64": f"data:image/png;base64,{img_to_b64(q_crop)}"
            })
            
        if c_img_box:
            c_img_box = [max(0, c_img_box[0]), max(0, c_img_box[1]), min(p_w, c_img_box[2]), min(p_h, c_img_box[3])]
            c_crop = page_img.crop(c_img_box)
            media.append({
                "type": "image",
                "label": "Choices",
                "base64": f"data:image/png;base64,{img_to_b64(c_crop)}"
            })
            
        final_questions.append({
            "id": q_id,
            "metadata": {
                "topic": "General",
                "major_category": "Pending Categorization",
                "source": source_label,
                "page": page_num
            },
            "content": {
                "question_text": "",
                "choices": {
                    "a": "See Diagram (A)",
                    "b": "See Diagram (B)",
                    "c": "See Diagram (C)",
                    "d": "See Diagram (D)"
                },
                "has_media": True,
                "media": media
            },
            "feedback": {
                "correct_answer": all_answers.get(q_num, "a"),
                "explanation": f"The correct answer for {q_id} is: See Diagram ({all_answers.get(q_num, 'a').upper()})."
            }
        })

    with open(args.output, 'w', encoding='utf-8') as f:
        for q in final_questions:
            f.write(json.dumps(q) + '\n')
            
    print(f"Successfully generated {len(final_questions)} questions in {args.output}")

if __name__ == "__main__":
    main()
