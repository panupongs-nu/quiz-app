import os
import json
import base64
from PIL import Image, ImageChops, ImageStat

# Base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_JSONL = os.path.join(BASE_DIR, '2025S_IP_Questions.jsonl')
OUTPUT_JSONL = os.path.join(BASE_DIR, '2025S_IP_Questions_Cropped.jsonl')
IMAGES_DIR = os.path.join(BASE_DIR, 'images/2025S_IP')

def get_islands(img):
    """
    Finds horizontal bands (islands) of non-white content.
    Returns a list of (top, bottom) y-coordinates.
    """
    width, height = img.size
    grayscale = img.convert('L')
    
    # Calculate horizontal projection (average brightness per row)
    # 255 = White, <255 = has content
    row_stats = []
    for y in range(height):
        row = grayscale.crop((0, y, width, y + 1))
        stat = ImageStat.Stat(row)
        row_stats.append(stat.mean[0])
    
    islands = []
    in_island = False
    start_y = 0
    
    threshold = 252 # Nearly white
    min_island_height = 40 # Ignore single lines of text
    
    for y, mean in enumerate(row_stats):
        if mean < threshold: # Not white
            if not in_island:
                start_y = y
                in_island = True
        else: # White
            if in_island:
                if (y - start_y) >= min_island_height:
                    islands.append((start_y, y))
                in_island = False
                
    if in_island and (height - start_y) >= min_island_height:
        islands.append((start_y, height))
        
    return islands

def smart_crop(image_path, question_id):
    if not os.path.exists(image_path):
        return None
        
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # Manual overrides from user
    manual_crops = {
        "2025S-Q1": (0.20, 0.40),
        "2025S-Q9": (0.20, 0.38),
        "2025S-Q10": (0.53, 0.71),
        "2025S-Q16": (0.22, 0.35),
        "2025S-Q26": (0.17, 0.58),
        "2025S-Q30": (0.18, 0.90),
        "2025S-Q51": (0.48, 0.92),
        "2025S-Q53": (0.44, 0.66),
    }
    
    if question_id in manual_crops:
        top_f, bottom_f = manual_crops[question_id]
        cropped = img.crop((0, int(top_f * height), width, int(bottom_f * height)))
        # Trim horizontal white space
        bg = Image.new(cropped.mode, cropped.size, (255, 255, 255))
        diff = ImageChops.difference(cropped, bg)
        bbox = diff.getbbox()
        if bbox:
            cropped = cropped.crop(bbox)
        return cropped

    # 1. Get all significant horizontal blocks for others
    islands = get_islands(img)
    
    if not islands:
        return img

    # 2. Heuristic: Match question to island based on position
    target_island = None
    
    if question_id == "2025S-Q10":
        # Usually the second major block on the page
        target_island = islands[1] if len(islands) > 1 else islands[-1]
    elif question_id in ["2025S-Q16", "2025S-Q26", "2025S-Q30", "2025S-Q51", "2025S-Q53"]:
        # Find the largest island which is likely the diagram
        target_island = max(islands, key=lambda x: x[1]-x[0])
    
    if target_island:
        # Crop vertically
        top, bottom = target_island
        # Add some vertical margin
        top = max(0, top - 10)
        bottom = min(height, bottom + 10)
        cropped = img.crop((0, top, width, bottom))
        
        # Now trim horizontally
        bg = Image.new(cropped.mode, cropped.size, (255, 255, 255))
        diff = ImageChops.difference(cropped, bg)
        bbox = diff.getbbox()
        if bbox:
            cropped = cropped.crop(bbox)
        return cropped

    return img

def main():
    with open(INPUT_JSONL, 'r', encoding='utf-8') as f_in, \
         open(OUTPUT_JSONL, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            q = json.loads(line)
            if q['content']['has_media']:
                page_num = q['metadata']['page']
                img_path = os.path.join(IMAGES_DIR, f"page-{page_num:02d}.png")
                
                cropped_img = smart_crop(img_path, q['id'])
                
                if cropped_img:
                    from io import BytesIO
                    buffered = BytesIO()
                    cropped_img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    q['content']['media'][0]['base64'] = f"data:image/png;base64,{img_str}"
            
            f_out.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"Created {OUTPUT_JSONL} with cropped diagrams.")

if __name__ == "__main__":
    main()
