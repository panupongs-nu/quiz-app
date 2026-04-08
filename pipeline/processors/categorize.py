import os
import subprocess
import re

# Mapping based on major_category.md
TAGS = {
    "CorporateAndLegalAffairs": "#1_CorporateAndLegalAffairs",
    "BusinessStrategy": "#2_BusinessStrategy",
    "SystemStrategy": "#3_SystemStrategy",
    "DevelopmentTechnology": "#4_DevelopmentTechnology",
    "ProjectManagement": "#5_ProjectManagement",
    "ServiceManagement": "#6_ServiceManagement",
    "BasicTheory": "#7_BasicTheory",
    "ComputerSystem": "#8_ComputerSystem",
    "TechnologyElement": "#9_TechnologyElement"
}

def get_category(q_text, q_num):
    q_text_lower = q_text.lower()
    
    # Field: Strategy (approx 66-100)
    if 66 <= q_num <= 100:
        # Check System Strategy (Items 18-24) - High Priority
        if any(kw in q_text_lower for kw in [
            "information system strategy", "master plan", "bpr", "bpm", "dfd", "workflow", 
            "saas", "paas", "iaas", "cloud", "literacy", "tco", "rfp", "rfi", "procurement", 
            "requirements definition", "computerization plan", "solution business"
        ]):
            return TAGS["SystemStrategy"]

        # Check Corporate & Legal Affairs (Items 1-8)
        if any(kw in q_text_lower for kw in [
            "compliance", "csr", "mission", "vision", "philosophy", "accounting", "financial", 
            "balance sheet", "p/l", "profit", "loss", "cost", "break-even", "copyright", 
            "patent", "trademark", "intellectual property", "labor", "ethics", "law", 
            "standardization", "iso", "stakeholder", "pl act", "worker dispatching", "accounting audit"
        ]):
            return TAGS["CorporateAndLegalAffairs"]
            
        # Default for Business Strategy (Items 9-17)
        return TAGS["BusinessStrategy"]

    # Field: Management (approx 46-65)
    if 46 <= q_num <= 50: return TAGS["DevelopmentTechnology"]
    if 51 <= q_num <= 57: return TAGS["ProjectManagement"]
    if 58 <= q_num <= 65: return TAGS["ServiceManagement"]

    # Field: Technology (approx 1-45)
    if 1 <= q_num <= 9: return TAGS["BasicTheory"]
    if 10 <= q_num <= 23: return TAGS["ComputerSystem"]
    if 24 <= q_num <= 45: return TAGS["TechnologyElement"]
    
    return "#Uncategorized"

def process_pdf(pdf_path):
    print(f"Processing {pdf_path}...")
    try:
        text = subprocess.check_output(["pdftotext", pdf_path, "-"], stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return {}

    parts = re.split(r'\n(Q\d+[\.\s]|\[Q\d+\])', text)
    
    results = {}
    for i in range(1, len(parts), 2):
        q_marker = parts[i]
        q_text = parts[i+1] if i+1 < len(parts) else ""
        
        match = re.search(r'Q(\d+)', q_marker)
        if match:
            q_num = int(match.group(1))
            if 1 <= q_num <= 100:
                results[q_num] = get_category(q_text, q_num)
                
    return results

def main():
    files = [f for f in os.listdir('itpec_exams') if 'Question' in f and f.endswith('.pdf')]
    files.sort(reverse=True) # Start from newest
    
    with open('categorized_questions.md', 'w') as out:
        out.write("# ITPE IP Categorized Questions\n\n")
        out.write("## Major Category Order\n")
        out.write("1. Corporate and Legal Affairs (#1_CorporateAndLegalAffairs)\n")
        out.write("2. Business Strategy (#2_BusinessStrategy)\n")
        out.write("3. System Strategy (#3_SystemStrategy)\n")
        out.write("4. Development Technology (#4_DevelopmentTechnology)\n")
        out.write("5. Project Management (#5_ProjectManagement)\n")
        out.write("6. Service Management (#6_ServiceManagement)\n")
        out.write("7. Basic Theory (#7_BasicTheory)\n")
        out.write("8. Computer System (#8_ComputerSystem)\n")
        out.write("9. Technology Element (#9_TechnologyElement)\n\n")
        
        for f in files:
            exam_name = f.replace('_Question.pdf', '').replace('_Questions.pdf', '')
            out.write(f"## {exam_name}\n")
            
            results = process_pdf(os.path.join('itpec_exams', f))
            if len(results) < 50:
                print(f"Only {len(results)} questions found in {f}, filling with defaults.")
                for q in range(1, 101):
                    if q not in results:
                        results[q] = get_category("", q)
            
            for q_num in range(1, 101):
                cat = results.get(q_num, get_category("", q_num))
                out.write(f"Q{q_num}: {cat}\n")
            out.write("\n")

if __name__ == "__main__":
    main()
