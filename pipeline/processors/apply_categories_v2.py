import json
import os

# Official ITPE Major Categories (as used in the quiz app's allCats)
CATEGORIES = [
    "1. Corporate and legal affairs",
    "2. Business Strategy",
    "3. System Strategy",
    "4. Development Strategy",
    "5. Project Management",
    "6. Service Management",
    "7. Basic Theory",
    "8. Computer System",
    "9. Technology Element"
]

def get_category_by_num(q_num):
    """
    Standard ITPE IP exam structure (100 questions):
    Questions 1-45: Technology (Strategy/Management sometimes interleaved but usually:)
    Questions 1-9: Basic Theory (Cat 7)
    Questions 10-23: Computer System (Cat 8)
    Questions 24-45: Technology Element (Cat 9)
    
    Questions 46-65: Management
    Questions 46-50: Development Strategy (Cat 4)
    Questions 51-57: Project Management (Cat 5)
    Questions 58-65: Service Management (Cat 6)
    
    Questions 66-100: Strategy
    Questions 66-73: System Strategy (Cat 3)
    Questions 74-82: Business Strategy (Cat 2)
    Questions 83-100: Corporate and legal affairs (Cat 1)
    
    Note: These ranges vary slightly by year but this is the general blueprint.
    """
    if 1 <= q_num <= 9: return CATEGORIES[6]   # 7. Basic Theory
    if 10 <= q_num <= 23: return CATEGORIES[7] # 8. Computer System
    if 24 <= q_num <= 45: return CATEGORIES[8] # 9. Technology Element
    if 46 <= q_num <= 50: return CATEGORIES[3] # 4. Development Strategy
    if 51 <= q_num <= 57: return CATEGORIES[4] # 5. Project Management
    if 58 <= q_num <= 65: return CATEGORIES[5] # 6. Service Management
    if 66 <= q_num <= 73: return CATEGORIES[2] # 3. System Strategy
    if 74 <= q_num <= 82: return CATEGORIES[1] # 2. Business Strategy
    if 83 <= q_num <= 100: return CATEGORIES[0]# 1. Corporate and legal affairs
    return "Other"

def apply_categories(jsonl_path):
    if not os.path.exists(jsonl_path):
        print(f"Error: {jsonl_path} not found.")
        return
        
    temp_path = jsonl_path + ".tmp"
    count = 0
    with open(jsonl_path, 'r', encoding='utf-8') as fin, \
         open(temp_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            q = json.loads(line)
            # Extract question number from ID (e.g., 2025S-Q-001 -> 1)
            q_num_match = os.path.basename(q['id']).split('-')[-1]
            q_num = int(q_num_match)
            
            q['metadata']['major_category'] = get_category_by_num(q_num)
            fout.write(json.dumps(q) + '\n')
            count += 1
            
    os.replace(temp_path, jsonl_path)
    print(f"Updated {count} categories in {jsonl_path}")

if __name__ == "__main__":
    files = [
        "data/processed_jsonl/2025S_IP_Questions.jsonl",
        "data/processed_jsonl/2024A_IP_Questions.jsonl",
        "data/processed_jsonl/2024S_IP_Questions.jsonl"
    ]
    for f in files:
        apply_categories(f)
