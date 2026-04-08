import os
import re

def classify_ocr_text(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Skip Page 1 and Page 2 (Cover and Disclaimers)
    page3_marker = "--- Page 3 ---"
    if page3_marker in content:
        content = content[content.find(page3_marker):]
        
    # Split by Q\d+.
    # Use same regex as generate_quiz_jsonl.py
    blocks = re.split(r'(?:^|\n)(Q\d+)\.\s+', content)
    
    results = []
    # blocks[0] is header info before Q1
    for i in range(1, len(blocks), 2):
        q_num_str = blocks[i]
        q_content = blocks[i+1]
        
        # Detect choices
        c_matches = list(re.finditer(r'(?:^|\n)\s*([a-d])[\)\.]', q_content))
        
        if c_matches:
            q_text = q_content[:c_matches[0].start()].strip()
            # Extract choices to see if they are complex
            choice_texts = []
            for j in range(len(c_matches)):
                start = c_matches[j].end()
                end = c_matches[j+1].start() if j+1 < len(c_matches) else len(q_content)
                choice_texts.append(q_content[start:end].strip())
        else:
            q_text = q_content.strip()
            choice_texts = []
            
        # Detect Question Part Type
        q_has_diagram = any(kw in q_text.lower() for kw in ['figure', 'diagram', 'graph', '!['])
        q_has_table = 'table' in q_text.lower() or '|' in q_text or '[data]' in q_text.lower() or '[program]' in q_text.lower()
        
        q_types = []
        if q_has_table: q_types.append("Table")
        if q_has_diagram: q_types.append("Diagram")
        if not q_types: q_types.append("Text")
        
        # Detect Choices Part Type
        o_types = []
        if not choice_texts:
            o_types.append("Unknown/Missing")
        else:
            # If choices are very short or look like placeholders
            if all(len(c) < 2 for c in choice_texts):
                o_types.append("Diagram (Likely)")
            # If choices contain table markers
            elif any('|' in c for c in choice_texts):
                o_types.append("Table")
            # If choices are multiline
            elif any('\n' in c for c in choice_texts):
                o_types.append("Multiline Text")
            else:
                o_types.append("Text")
                
        results.append({
            'id': q_num_str,
            'q_type': " + ".join(q_types),
            'o_type': " + ".join(o_types),
            'preview': " | ".join(choice_texts).replace('\n', ' ')[:50]
        })
        
    return results

def save_report(results, output_path):
    lines = ["Question ID\tQuestion Part\tChoices Part\tChoices Preview"]
    lines.append("-" * 100)
    for r in results:
        # Avoid double Q if the ID already starts with Q
        q_label = r['id'] if r['id'].startswith('Q') else f"Q{r['id']}"
        lines.append(f"{q_label}\t{r['q_type']:<20}\t{r['o_type']:<20}\t{r['preview']}...")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Created {output_path}")

if __name__ == "__main__":
    results_2025A = classify_ocr_text('2025A_IP_Questions_OCR.txt')
    save_report(results_2025A, "classification_2025A.txt")
    
    results_2025S = classify_ocr_text('2025S_IP_Questions_OCR.txt')
    save_report(results_2025S, "classification_2025S.txt")
