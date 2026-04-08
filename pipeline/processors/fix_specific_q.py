import json
import os

def fix_specific_questions(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    # Update choices for specific questions
    q1_choices = {
        "a": "(A ∪ B) is a subset of the complement of (A ∩ B).",
        "b": "(A ∪ B) is a subset of A.",
        "c": "(A ∩ B) is a subset of (A ∪ B).",
        "d": "(A ∩ B) is a subset of the complement of A."
    }
    
    q3_text_table = """
| | Mean | Median |
| :--- | :--- | :--- |
| a) | 20 | 40 |
| b) | 40 | 20 |
| c) | 300 | 20 |
| d) | 300 | 40 |
"""

    q6_text_table = """
| | A | B |
| :--- | :--- | :--- |
| a) | 5000 | 0.2 |
| b) | 5000 | 0.8 |
| c) | 5250 | 0.2 |
| d) | 5250 | 0.8 |
"""

    q8_text_table = """
| | A | B |
| :--- | :--- | :--- |
| a) | 1 | arr[i + 1] |
| b) | 1 | arr[i - 1] |
| c) | 2 | arr[i + 1] |
| d) | 2 | arr[i - 1] |
"""

    q21_text_table = """
| | A | B | C | D | E |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | | **Weather type** | **Sunny** | **Cloudy** | **Rainy** | |
| **2** | | **Probability** | 0.5 | 0.3 | 0.2 | |
| **3** | **Product** | **Sunny** | **Cloudy** | **Rainy** | **Predicted** |
| **4** | Product A | 300,000 | 100,000 | 80,000 | |
| **5** | Product B | 250,000 | 280,000 | 300,000 | |
| **6** | Product C | 100,000 | 250,000 | 350,000 | |
"""

    q68_text_table = """
| | Store C | Store D |
| :--- | :---: | :---: |
| Warehouse A | 400 | 200 |
| Warehouse B | 200 | 100 |
"""

    q72_text_table = """
| Item | Value |
| :--- | :--- |
| Sales amount | 2,000,000 yen |
| Unit sales price | 1,000 yen |
| Units sold | 2,000 |
| Fixed cost | 600,000 yen |
| Variable cost per unit | 700 yen |
"""

    q97_text_table = """
| Evaluation item | Weight | Vendor A | Vendor B | Vendor C | Vendor D |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Management viewpoint | 2 | 2 | 4 | 3 | 3 |
| Technology viewpoint | 3 | 3 | 4 | 2 | 3 |
| Price viewpoint | 5 | 4 | 2 | 4 | 3 |
"""

    temp_path = file_path + ".fix"
    with open(file_path, 'r', encoding='utf-8') as f_in, \
         open(temp_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if not line.strip(): continue
            q = json.loads(line)
            
            fixed = False
            # Check for new ID format
            if q['id'] == "2025A-Q-001":
                q['content']['choices'] = q1_choices
                fixed = True
            elif q['id'] == "2025A-Q-003":
                if q3_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q3_text_table
                q['content']['choices'] = {"a": "Mean: 20, Median: 40", "b": "Mean: 40, Median: 20", "c": "Mean: 300, Median: 20", "d": "Mean: 300, Median: 40"}
                q['content']['has_media'] = False
                q['content']['media'] = []
                fixed = True
            elif q['id'] == "2025A-Q-006":
                if q6_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q6_text_table
                q['content']['choices'] = {"a": "A: 5000, B: 0.2", "b": "A: 5000, B: 0.8", "c": "A: 5250, B: 0.2", "d": "A: 5250, B: 0.8"}
                fixed = True
            elif q['id'] == "2025A-Q-008":
                if q8_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q8_text_table
                q['content']['choices'] = {"a": "A: 1, B: arr[i + 1]", "b": "A: 1, B: arr[i - 1]", "c": "A: 2, B: arr[i + 1]", "d": "A: 2, B: arr[i - 1]"}
                fixed = True
            elif q['id'] == "2025A-Q-021":
                if q21_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q21_text_table
                fixed = True
            elif q['id'] == "2025A-Q-068":
                if q68_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q68_text_table
                fixed = True
            elif q['id'] == "2025A-Q-072":
                if q72_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q72_text_table
                q['content']['choices'] = {"a": "2,400", "b": "2,500", "c": "4,800", "d": "6,000"}
                fixed = True
            elif q['id'] == "2025A-Q-097":
                if q97_text_table not in q['content']['question_text']:
                    q['content']['question_text'] += q97_text_table
                q['content']['choices'] = {"a": "Vendor A", "b": "Vendor B", "c": "Vendor C", "d": "Vendor D"}
                fixed = True
            elif q['id'] == "2025A-Q-092":
                q['content']['choices'] = {"a": "See Diagram (a)", "b": "See Diagram (b)", "c": "See Diagram (c)", "d": "See Diagram (d)"}
                fixed = True
            elif q['id'] == "2025S-Q-030":
                q['content']['choices'] = {"a": "See Diagram (a)", "b": "See Diagram (b)", "c": "See Diagram (c)", "d": "See Diagram (d)"}
                fixed = True
            elif q['id'] == "2025A-Q-032":
                q['content']['question_text'] = "Which of the following is the appropriate description of a SIM card?"
                fixed = True
            elif q['id'] == "2025A-Q-071":
                q['content']['question_text'] = "Which of the following is the expression that calculates operating profit?"
                fixed = True
            
            if fixed:
                print(f"Fixed {q['id']}")
                ans = q['feedback']['correct_answer']
                choice_text = q['content']['choices'].get(ans, "")
                q['feedback']['explanation'] = f"The correct answer for {q['id']} is: {choice_text}."

            f_out.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    os.rename(temp_path, file_path)

if __name__ == "__main__":
    fix_specific_questions('2025A_IP_Questions.jsonl')
