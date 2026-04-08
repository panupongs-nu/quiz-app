import numpy as np
from PIL import Image, ImageChops, ImageStat
from skimage import measure, feature
import os

def get_vertical_profile(img):
    img_np = np.array(img.convert('L'))
    inverted = 255 - img_np
    return np.mean(inverted, axis=1)

def get_text_lines(img, threshold=1.5, min_gap=5):
    profile = get_vertical_profile(img)
    lines = []
    in_line = False
    start_y = 0
    for y, val in enumerate(profile):
        if val > threshold:
            if not in_line:
                start_y = y
                in_line = True
        else:
            if in_line:
                lookahead = profile[y:y+min_gap]
                if len(lookahead) == 0 or np.max(lookahead) <= threshold:
                    lines.append((start_y, y))
                    in_line = False
    if in_line:
        lines.append((start_y, len(profile)))
    return lines

def analyze_complexity(img, top, bottom):
    cropped = img.crop((0, top, img.size[0], bottom))
    img_np = np.array(cropped.convert('L'))
    edges = feature.canny(img_np, sigma=1)
    labels = measure.label(edges)
    props = measure.regionprops(labels)
    if not props:
        return 0
    max_area = max([p.area for p in props])
    return max_area

def get_content_islands(img, threshold=2.0, margin=5):
    profile = get_vertical_profile(img)
    islands = []
    in_island = False
    start_y = 0
    for y, val in enumerate(profile):
        if val > threshold:
            if not in_island:
                start_y = y
                in_island = True
        else:
            if in_island:
                lookahead = profile[y:y+margin]
                if len(lookahead) == 0 or np.max(lookahead) <= threshold:
                    islands.append((start_y, y))
                    in_island = False
    if in_island:
        islands.append((start_y, len(profile)))
    return islands

def smart_crop_v2(img, q_id):
    width, height = img.size
    # Ignore headers/footers
    margin_y = int(height * 0.1)
    
    # We find all blocks of content
    islands = get_content_islands(img.crop((0, margin_y, width, height - margin_y)))
    islands = [(t + margin_y, b + margin_y) for t, b in islands]
    
    if not islands:
        return None
        
    # We are looking for something that is NOT just a single line of text
    # AND has high complexity
    candidates = []
    for top, bottom in islands:
        h = bottom - top
        complexity = analyze_complexity(img, top, bottom)
        
        # A diagram is usually either very tall OR has a large max connected edge component
        # threshold 150 area for max connected component is good for diagrams
        if h > 40 and complexity > 150:
            candidates.append((complexity, top, bottom))
            
    if not candidates:
        return None
        
    # Sort by complexity
    best_score, top, bottom = max(candidates, key=lambda x: x[0])
    
    # Precise crop and trim
    cropped = img.crop((0, max(0, top - 10), width, min(height, bottom + 10)))
    bg = Image.new(cropped.mode, cropped.size, (255, 255, 255))
    diff = ImageChops.difference(cropped, bg)
    bbox = diff.getbbox()
    if bbox:
        p = 5
        bbox = (max(0, bbox[0]-p), max(0, bbox[1]-p), 
                min(cropped.size[0], bbox[2]+p), min(cropped.size[1], bbox[3]+p))
        cropped = cropped.crop(bbox)
        
    return cropped
