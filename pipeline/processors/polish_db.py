import json
import os

def polish_db():
    # Fix 2025S-Q7
    with open('2025S_IP_Questions.jsonl', 'r', encoding='utf-8') as f:
        s_lines = f.readlines()
    
    with open('2025S_IP_Questions.jsonl', 'w', encoding='utf-8') as f:
        for line in s_lines:
            q = json.loads(line)
            if q['id'] == "2025S-Q7":
                q['content']['choices'] = {
                    "a": "A: (i mod 2 ≠ 0) and (j mod 2 ≠ 0), B: '+', C: i",
                    "b": "A: (i mod 2 ≠ 0) and (j mod 2 ≠ 0), B: i, C: '+'",
                    "c": "A: (i mod 2 = 0) and (j mod 2 = 0), B: '+', C: i",
                    "d": "A: (i mod 2 = 0) and (j mod 2 = 0), B: i, C: '+'"
                }
            
            # Recalculate explanation to be safe
            ans = q['feedback']['correct_answer']
            choice_text = q['content']['choices'].get(ans, "")
            q['feedback']['explanation'] = f"The correct answer for {q['id']} is: {choice_text}."
            
            f.write(json.dumps(q, ensure_ascii=False) + '\n')

    # Fix 2025A
    with open('2025A_IP_Questions.jsonl', 'r', encoding='utf-8') as f:
        a_lines = f.readlines()
        
    with open('2025A_IP_Questions.jsonl', 'w', encoding='utf-8') as f:
        for line in a_lines:
            q = json.loads(line)
            
            if q['id'] == "2025A-Q31":
                q['content']['choices'] = {
                    "a": "Cookie",
                    "b": "RAID",
                    "c": "Online storage",
                    "d": "Crawler"
                }
            elif q['id'] == "2025A-Q70":
                q['content']['choices'] = {
                    "a": "ABC analysis",
                    "b": "SWOT analysis",
                    "c": "Environmental assessment",
                    "d": "Risk assessment"
                }
            
            # Recalculate explanation
            ans = q['feedback']['correct_answer']
            choice_text = q['content']['choices'].get(ans, "")
            q['feedback']['explanation'] = f"The correct answer for {q['id']} is: {choice_text}."
            
            f.write(json.dumps(q, ensure_ascii=False) + '\n')

    print("Database polished successfully.")

polish_db()
