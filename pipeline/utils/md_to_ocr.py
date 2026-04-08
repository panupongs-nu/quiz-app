import re
import os

def convert_md_to_ocr_format(md_path, txt_path):
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by Question Number
    # Use non-capturing group for start of line or file
    blocks = re.split(r'(?:^|\n)- Question Number: (\d+)', content)
    
    output = []
    # blocks[0] is header
    for i in range(1, len(blocks), 2):
        q_num = blocks[i]
        q_content = blocks[i+1]
        
        # We want to format it as:
        # Q1. [Everything else]
        # But we should clean up the "- Question Text:" and "- Options:" labels to look like OCR
        
        clean_content = q_content
        clean_content = clean_content.replace("- Question Text: ", "")
        # Replace "- Options: " with a newline to start options
        clean_content = clean_content.replace("- Options: ", "\n")
        # Remove "Correct Answer" and "Category Tag" as they aren't in OCR
        clean_content = re.sub(r'- Correct Answer:.*', '', clean_content)
        clean_content = re.sub(r'- Category Tag:.*', '', clean_content)
        
        # If options are a), b), c), d) in the same line, put them on new lines
        # This helps the later regex
        clean_content = re.sub(r',\s*([a-d]\))', r'\n\1', clean_content)
        
        output.append(f"Q{q_num}. {clean_content.strip()}\n\n")
        
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("".join(output))
    print(f"Created {txt_path}")

if __name__ == "__main__":
    convert_md_to_ocr_format('2025S_IP_Categorized.md', '2025S_IP_Questions_OCR.txt')
