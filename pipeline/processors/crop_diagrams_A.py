import os
import json
import base64
from PIL import Image, ImageChops

# Base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_JSONL = os.path.join(BASE_DIR, '2025A_IP_Questions.jsonl')
OUTPUT_JSONL = os.path.join(BASE_DIR, '2025A_IP_Questions_Cropped.jsonl')
IMAGES_DIR = os.path.join(BASE_DIR, 'pages')

def auto_crop_diagram(image_path, question_num):
    if not os.path.exists(image_path):
        return None
        
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # Heuristics for 2025A (Autumn) diagrams:
    crops = {
        "2025A-Q3": (0.05, 0.20, 0.95, 0.50),   # Table for Q3
        "2025A-Q7": (0.05, 0.30, 0.95, 0.60),   # Logic diagrams
        "2025A-Q9": (0.05, 0.20, 0.95, 0.45),   # Logic diagrams
        "2025A-Q10": (0.05, 0.60, 0.95, 0.85),  # Logic diagrams (same page as Q9)
        "2025A-Q14": (0.05, 0.15, 0.95, 0.45),  # Duplex system
        "2025A-Q25": (0.05, 0.25, 0.95, 0.60),  # Relational database tables
        "2025A-Q29": (0.05, 0.15, 0.95, 0.45),  # Firewall diagram
        "2025A-Q30": (0.05, 0.55, 0.95, 0.80),  # Network diagram (same page as Q29)
        "2025A-Q52": (0.05, 0.15, 0.95, 0.45),  # Arrow diagram
        "2025A-Q55": (0.05, 0.20, 0.95, 0.55),  # Gantt chart
        "2025A-Q90": (0.05, 0.15, 0.95, 0.45),  # Logic flowchart
        "2025A-Q94": (0.05, 0.25, 0.95, 0.55),  # Relational database tables
    }
    
    if question_num in crops:
        l, t, r, b = crops[question_num]
        crop_box = (int(l*width), int(t*height), int(r*width), int(b*height))
        cropped_img = img.crop(crop_box)
        
        # Further trim white space
        bg = Image.new(cropped_img.mode, cropped_img.size, (255, 255, 255))
        diff = ImageChops.difference(cropped_img, bg)
        bbox = diff.getbbox()
        if bbox:
            padding = 10
            bbox = (max(0, bbox[0]-padding), max(0, bbox[1]-padding), 
                    min(width, bbox[2]+padding), min(height, bbox[3]+padding))
            cropped_img = cropped_img.crop(bbox)
        return cropped_img
    
    return img

def main():
    with open(INPUT_JSONL, 'r', encoding='utf-8') as f_in, \
         open(OUTPUT_JSONL, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            q = json.loads(line)
            if q['content']['has_media']:
                page_num = q['metadata']['page']
                img_path = os.path.join(IMAGES_DIR, f"page-{page_num:02d}.jpg")
                
                cropped_img = auto_crop_diagram(img_path, q['id'])
                
                if cropped_img:
                    from io import BytesIO
                    buffered = BytesIO()
                    cropped_img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    q['content']['media'][0]['base64'] = f"data:image/jpeg;base64,{img_str}"
            
            f_out.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"Created {OUTPUT_JSONL} with cropped diagrams.")

if __name__ == "__main__":
    main()
