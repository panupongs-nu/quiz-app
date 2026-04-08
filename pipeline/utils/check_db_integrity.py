import json
import os

def check_integrity(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print(f"--- Integrity Report for {file_path} ---")
    
    ids = []
    issues = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if len(lines) != 100:
        issues.append(f"Count mismatch: Expected 100 questions, found {len(lines)}.")
    
    for i, line in enumerate(lines):
        try:
            q = json.loads(line)
            q_id = q.get('id', f"Unknown-Line-{i+1}")
            ids.append(q_id)
            
            # Check empty text
            if not q.get('content', {}).get('question_text'):
                issues.append(f"[{q_id}] Empty question_text")
            
            # Check choices
            choices = q.get('content', {}).get('choices', {})
            if not choices:
                issues.append(f"[{q_id}] Missing choices object")
            else:
                for letter in ['a', 'b', 'c', 'd']:
                    val = choices.get(letter)
                    if val == "N/A" or not val:
                        issues.append(f"[{q_id}] Choice {letter} is '{val}'")
            
            # Check correct answer
            ans = q.get('feedback', {}).get('correct_answer')
            if ans not in ['a', 'b', 'c', 'd']:
                issues.append(f"[{q_id}] Invalid correct_answer: '{ans}'")
                
            # Check explanation
            expl = q.get('feedback', {}).get('explanation')
            if not expl or expl == "N/A":
                issues.append(f"[{q_id}] Missing or N/A explanation")
            elif q_id not in expl:
                # Basic check if explanation mentions the wrong Q number
                issues.append(f"[{q_id}] Explanation might be wrong (mentions {expl.split(' ')[4] if len(expl.split(' ')) > 4 else '?'})")

            # Check media
            if q.get('content', {}).get('has_media'):
                media = q.get('content', {}).get('media', [])
                if not media:
                    issues.append(f"[{q_id}] has_media is true but media array is empty")
                else:
                    for m in media:
                        if not m.get('base64'):
                            issues.append(f"[{q_id}] Broken media: missing base64")

        except Exception as e:
            issues.append(f"Line {i+1}: Failed to parse JSON: {str(e)}")
            
    # Check duplicate IDs
    if len(ids) != len(set(ids)):
        duplicates = [x for x in set(ids) if ids.count(x) > 1]
        issues.append(f"Duplicate IDs found: {duplicates}")
        
    if not issues:
        print("✅ No issues found.")
    else:
        print(f"❌ Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"  - {issue}")
    print("\n")

check_integrity('2025S_IP_Questions.jsonl')
check_integrity('2025A_IP_Questions.jsonl')
