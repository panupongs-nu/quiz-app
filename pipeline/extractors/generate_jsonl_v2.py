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
    # Fallback
    def img_to_b64(img, format="PNG"):
        from io import BytesIO
        import base64
        buffered = BytesIO()
        img.save(buffered, format=format)
        return base64.b64encode(buffered.getvalue()).decode()

def get_answers(answers_path):
    answers = {}
    if not os.path.exists(answers_path):
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

def get_bbox(items):
    valid = [it for it in items if "bounding box" in it and len(it["bounding box"]) == 4]
    if not valid: return None
    return [
        min(it["bounding box"][0] for it in valid),
        min(it["bounding box"][1] for it in valid),
        max(it["bounding box"][2] for it in valid),
        max(it["bounding box"][3] for it in valid)
    ]

def main():
    parser = argparse.ArgumentParser(description="Generate JSONL using coordinate-based structural analysis.")
    parser.add_argument("--year", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--answers", required=True)
    parser.add_argument("--pages_dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source_name", default=None)
    args = parser.parse_args()
    
    if not os.path.exists(args.json): return
    with open(args.json, 'r') as f: data = json.load(f)
    all_answers = get_answers(args.answers)
    source_label = args.source_name or f"IT Passport {args.year}"
    
    flat_items = flatten_json(data["kids"])
    
    # Identify All Question Markers (Q1., Q2., etc.)
    q_markers = []
    for it in flat_items:
        content = str(it.get("content", ""))
        if re.match(r"^Q\d+\.", content) and it.get("page number", 0) >= 3:
            q_markers.append(it)
    
    # Calculate Page Height per page (if it varies, otherwise assume A4)
    page_heights = {}
    for it in flat_items:
        p = it.get("page number")
        if p and "bounding box" in it:
            page_heights[p] = max(page_heights.get(p, 841.89), it["bounding box"][3])

    final_questions = []
    print(f"Analyzing {len(q_markers)} questions for {args.year} using coordinate bounds...")
    
    for idx, q_marker in enumerate(q_markers):
        q_num = int(re.match(r"^Q(\d+)\.", q_marker["content"]).group(1))
        page_num = q_marker["page number"]
        q_id = f"{args.year}-Q-{q_num:03d}"
        q_top_limit = q_marker["bounding box"][3]
        
        # Find the next question on the SAME page to establish the bottom limit
        next_q_on_page = None
        for i in range(idx + 1, len(q_markers)):
            if q_markers[i]["page number"] == page_num:
                next_q_on_page = q_markers[i]
                break
        
        # Bottom limit: next question top OR footer safe zone (60pt)
        q_bottom_limit = next_q_on_page["bounding box"][3] if next_q_on_page else 60
        
        # 1. Collect all items that physically belong to this question block
        block_items = []
        for it in flat_items:
            if it.get("page number") == page_num and "bounding box" in it:
                it_box = it["bounding box"]
                # Vertical filter: Between this Q top and next Q top
                if it_box[1] >= q_bottom_limit - 5 and it_box[3] <= q_top_limit + 5:
                    if it.get("type") not in ["header", "footer"]:
                        # Exclude items that look like page numbers (e.g., "- 3 -" or "15")
                        content = str(it.get("content", "")).strip()
                        if not re.match(r"^–?\s*\d+\s*–?$", content):
                            block_items.append(it)
        
        # 2. Identify the Choice Start Point (a) marker)
        split_y = None
        for it in block_items:
            content = str(it.get("content", ""))
            if re.match(r'^\s*[a-d][\)\.]', content):
                # The top of the choices section is defined by the top of the first choice marker
                if split_y is None or it["bounding box"][3] > split_y:
                    split_y = it["bounding box"][3]
        
        # 3. Partition block items into Question part and Choice part
        if split_y is None:
            question_items = block_items
            choice_items = []
        else:
            # Shift split_y slightly up to include the choice marker itself in choices
            question_items = [it for it in block_items if it["bounding box"][1] >= split_y - 2]
            choice_items = [it for it in block_items if it["bounding box"][1] < split_y - 2]
        
        # 4. Generate Bboxes and Crops
        page_img_path = os.path.join(args.pages_dir, f"page-{page_num:02d}.jpg")
        if not os.path.exists(page_img_path): continue
        page_img = Image.open(page_img_path)
        p_w, p_h = page_img.size
        pdf_h = page_heights.get(page_num, 841.89)
        
        def to_img(pdf_box):
            if not pdf_box: return None
            l, b, r, t = pdf_box
            sx, sy = p_w / 595.27, p_h / pdf_h
            # Clamp to page bounds with 10px padding
            pad = 10
            box = [
                max(0, int(l * sx) - pad),
                max(0, int((pdf_h - t) * sy) - pad),
                min(p_w, int(r * sx) + pad),
                min(p_h, int((pdf_h - b) * sy) + pad)
            ]
            if box[2] <= box[0] or box[3] <= box[1]: return None
            return box

        q_img_box = to_img(get_bbox(question_items))
        c_img_box = to_img(get_bbox(choice_items))
        
        media = []
        if q_img_box:
            media.append({
                "type": "image", "label": "Question",
                "base64": f"data:image/png;base64,{img_to_b64(page_img.crop(q_img_box))}"
            })
        if c_img_box:
            media.append({
                "type": "image", "label": "Choices",
                "base64": f"data:image/png;base64,{img_to_b64(page_img.crop(c_img_box))}"
            })
            
        final_questions.append({
            "id": q_id,
            "metadata": {"topic": "General", "major_category": "Pending", "source": source_label, "page": page_num},
            "content": {
                "question_text": "", "has_media": True, "media": media,
                "choices": {"a": "See Diagram (A)", "b": "See Diagram (B)", "c": "See Diagram (C)", "d": "See Diagram (D)"}
            },
            "feedback": {
                "correct_answer": all_answers.get(q_num, "a"),
                "explanation": f"The correct answer for {q_id} is: See Diagram ({all_answers.get(q_num, 'a').upper()})."
            }
        })

    with open(args.output, 'w', encoding='utf-8') as f:
        for q in final_questions: f.write(json.dumps(q) + '\n')
    print(f"Generated {len(final_questions)} questions in {args.output}")

if __name__ == "__main__": main()
