import json
import os
import re

# Official BOK Categories (9 Major Categories with Numbers)
TAG_MAP = {
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

# Add some common name variations
NAME_MAP = {
    "Corporate and legal affairs": "1. Corporate and legal affairs",
    "Business Strategy": "2. Business Strategy",
    "Management Strategy": "2. Business Strategy",
    "System Strategy": "3. System Strategy",
    "Development Strategy": "4. Development Strategy",
    "Development Technology": "4. Development Strategy",
    "Project Management": "5. Project Management",
    "Service Management": "6. Service Management",
    "System Audit": "6. Service Management",
    "Basic Theory": "7. Basic Theory",
    "Computer System": "8. Computer System",
    "Computer Systems": "8. Computer System",
    "Technology Element": "9. Technology Element"
}

def load_categories_from_md(md_path):
    cats = {}
    if not os.path.exists(md_path):
        return cats
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        blocks = re.split(r'- Question Number: (\d+)', content)
        for i in range(1, len(blocks), 2):
            q_num = int(blocks[i])
            body = blocks[i+1]
            tag_match = re.search(r'- Category Tag: (#\w+)', body)
            if tag_match:
                tag = tag_match.group(1)
                cats[q_num] = TAG_MAP.get(tag, TAG_MAP["#Unknown"])
    return cats

# Hardcoded for 2025A Q51-100 since they were in generate_51_100.py
A_51_100 = {
    51: "#ProjectManagement", 52: "#ProjectManagement", 53: "#ProjectManagement", 54: "#ProjectManagement",
    55: "#ProjectManagement", 56: "#BasicTheory", 57: "#ProjectManagement", 58: "#ServiceManagement",
    59: "#ServiceManagement", 60: "#ServiceManagement", 61: "#ServiceManagement", 62: "#ServiceManagement",
    63: "#SystemAudit", 64: "#SystemStrategy", 65: "#CorporateLegalAffairs", 66: "#BasicTheory",
    67: "#CorporateLegalAffairs", 68: "#ManagementStrategy", 69: "#ManagementStrategy", 70: "#ManagementStrategy",
    71: "#CorporateLegalAffairs", 72: "#CorporateLegalAffairs", 73: "#ManagementStrategy", 74: "#ManagementStrategy",
    75: "#ManagementStrategy", 76: "#ManagementStrategy", 77: "#ManagementStrategy", 78: "#ManagementStrategy",
    79: "#ManagementStrategy", 80: "#ManagementStrategy", 81: "#ManagementStrategy", 82: "#ManagementStrategy",
    83: "#ManagementStrategy", 84: "#ManagementStrategy", 85: "#ManagementStrategy", 86: "#ManagementStrategy",
    87: "#ManagementStrategy", 88: "#ManagementStrategy", 89: "#ManagementStrategy", 90: "#ManagementStrategy",
    91: "#ManagementStrategy", 92: "#ManagementStrategy", 93: "#CorporateLegalAffairs", 94: "#CorporateLegalAffairs",
    95: "#CorporateLegalAffairs", 96: "#CorporateLegalAffairs", 97: "#CorporateLegalAffairs", 98: "#CorporateLegalAffairs",
    99: "#CorporateLegalAffairs", 100: "#CorporateLegalAffairs"
}

def fix_jsonl(file_path):
    if not os.path.exists(file_path):
        return
    
    # Load specific maps for this session
    cats_2025A = load_categories_from_md('2025A_IP_Categorized.md')
    cats_2025S = load_categories_from_md('2025S_IP_Categorized.md')
    
    # Merge A_51_100 into cats_2025A
    for q_num, tag in A_51_100.items():
        cats_2025A[q_num] = TAG_MAP.get(tag, TAG_MAP["#Unknown"])

    temp_path = file_path + ".tmp"
    fixed_count = 0
    with open(file_path, 'r', encoding='utf-8') as f_in, \
         open(temp_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if not line.strip(): continue
            q = json.loads(line)
            
            q_id = q.get('id', '')
            # Determine source and number
            # e.g., 2025A-Q-001
            parts = q_id.split('-')
            if len(parts) == 3:
                year_code = parts[0] # 2025A or 2025S
                q_num = int(parts[2])
                
                new_cat = None
                if year_code == "2025A":
                    new_cat = cats_2025A.get(q_num)
                elif year_code == "2025S":
                    new_cat = cats_2025S.get(q_num)
                
                if new_cat:
                    q['metadata']['major_category'] = new_cat
                    fixed_count += 1
                else:
                    # Fallback to existing map cleaning
                    current = q['metadata'].get('major_category', '')
                    cleaned = NAME_MAP.get(current, current)
                    if cleaned in TAG_MAP.values():
                        q['metadata']['major_category'] = cleaned
                    else:
                        q['metadata']['major_category'] = "10. Other (Categorization Pending)"
            
            f_out.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    os.rename(temp_path, file_path)
    print(f"Fixed {fixed_count} categories in {file_path}")

if __name__ == "__main__":
    fix_jsonl('2025S_IP_Questions.jsonl')
    fix_jsonl('2025A_IP_Questions.jsonl')
    fix_jsonl('questions_51_100.jsonl')
