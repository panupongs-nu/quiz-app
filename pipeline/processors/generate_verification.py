import json
import os

def generate_verification_report():
    json_path = "opendataloader_test/2025A_IP_Questions.json"
    if not os.path.exists(json_path):
        print("JSON file not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # We will look at Page 3 specifically as it has a mix of types
    page3_items = []
    def find_on_page(item, page=3):
        if isinstance(item, dict):
            if item.get("page number") == page:
                page3_items.append(item)
            for k in item.get("kids", []):
                find_on_page(k, page)
        elif isinstance(item, list):
            for i in item:
                find_on_page(i, page)

    find_on_page(data["kids"])

    report = ["# OpenDataLoader Verification Report - Page 3\n"]
    
    # The structure we saw was a top-level list containing questions
    for item in page3_items:
        if item.get("type") == "list" and item.get("level") == "6":
            for q_item in item.get("list items", []):
                content = q_item.get("content", "")
                if not content.startswith("Q"): continue
                
                q_id = content.split(".")[0]
                report.append(f"## {content}")
                report.append(f"- **Type**: {q_item.get('type')}")
                report.append(f"- **Bounding Box**: {q_item.get('bounding box')}")
                
                # Check for nested structures (Choices or Tables)
                for kid in q_item.get("kids", []):
                    if kid.get("type") == "list":
                        report.append("  - **Choices Detected (List)**:")
                        for choice in kid.get("list items", []):
                            report.append(f"    - {choice.get('content')}")
                    elif kid.get("type") == "table":
                        report.append(f"  - **Table Detected**: {kid.get('number of rows')}x{kid.get('number of columns')}")
                        report.append(f"    - **Table Box**: {kid.get('bounding box')}")
                report.append("\n")

    with open("workflow/VERIFICATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print("Created workflow/VERIFICATION_REPORT.md")

if __name__ == "__main__":
    generate_verification_report()
