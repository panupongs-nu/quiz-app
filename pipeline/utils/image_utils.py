import os
import base64
import numpy as np
from io import BytesIO
from PIL import Image, ImageChops, ImageStat
from layout_utils import get_content_islands, analyze_complexity, smart_crop_v2

def smart_crop(img, question_id):
    """
    Finds the diagram on the page.
    This version uses the layout-aware anchor search.
    """
    # Use the new v2 algorithm
    cropped = smart_crop_v2(img, question_id)
    if cropped:
        return cropped
    
    # Fallback to old behavior if v2 fails
    width, height = img.size
    # Ignore top/bottom 10%
    margin = int(height * 0.1)
    
    islands = get_content_islands(img.crop((0, margin, width, height - margin)))
    islands = [(top + margin, bottom + margin) for top, bottom in islands]
    
    if not islands:
        return img
        
    island_scores = []
    for top, bottom in islands:
        score = analyze_complexity(img, top, bottom)
        island_scores.append((score, top, bottom))
        
    best_score, best_top, best_bottom = max(island_scores, key=lambda x: x[0])
    
    # Manual overrides still supported for tricky ones
    manual_crops_s = {
        "2025S-Q-001": (0.20, 0.40),
        "2025S-Q-009": (0.20, 0.38),
        "2025S-Q-010": (0.53, 0.71),
        "2025S-Q-016": (0.22, 0.35),
        "2025S-Q-026": (0.17, 0.58),
        "2025S-Q-030": (0.18, 0.90),
        "2025S-Q-051": (0.48, 0.92),
        "2025S-Q-053": (0.44, 0.66),
    }
    # Manual overrides for 2025A (Format: Q-XXX)
    manual_crops_a = {
        "2025A-Q-003": (0.05, 0.10, 0.95, 0.25),
        "2025A-Q-006": (0.05, 0.60, 0.95, 0.95), 
        "2025A-Q-007": (0.05, 0.30, 0.95, 0.60),
        "2025A-Q-008": (0.05, 0.60, 0.95, 0.95),
        "2025A-Q-009": (0.05, 0.20, 0.95, 0.45),
        "2025A-Q-010": (0.05, 0.60, 0.95, 0.85),
        "2025A-Q-012": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-013": (0.05, 0.50, 0.95, 0.70),
        "2025A-Q-014": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-016": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-018": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-021": (0.05, 0.15, 0.95, 0.65),
        "2025A-Q-025": (0.05, 0.25, 0.95, 0.60),
        "2025A-Q-026": (0.05, 0.25, 0.95, 0.60),
        "2025A-Q-027": (0.05, 0.25, 0.95, 0.60),
        "2025A-Q-028": (0.05, 0.25, 0.95, 0.60),
        "2025A-Q-029": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-030": (0.05, 0.55, 0.95, 0.80),
        "2025A-Q-036": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-040": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-041": (0.05, 0.22, 0.95, 0.35),
        "2025A-Q-052": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-055": (0.05, 0.20, 0.95, 0.55),
        "2025A-Q-056": (0.05, 0.15, 0.95, 0.85),
        "2025A-Q-059": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-064": (0.05, 0.50, 0.95, 0.68),
        "2025A-Q-068": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-072": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-090": (0.05, 0.15, 0.95, 0.45),
        "2025A-Q-092": (0.05, 0.15, 0.95, 0.60),
        "2025A-Q-094": (0.05, 0.25, 0.95, 0.55),
        "2025A-Q-097": (0.05, 0.15, 0.95, 0.85),
        "2025A-Q-099": (0.05, 0.15, 0.95, 0.45),
    }

    final_top, final_bottom = best_top, best_bottom
    
    if question_id in manual_crops_s:
        top_f, bottom_f = manual_crops_s[question_id]
        final_top, final_bottom = int(top_f * height), int(bottom_f * height)
    elif question_id in manual_crops_a:
        l, t, r, b = manual_crops_a[question_id]
        cropped = img.crop((int(l*width), int(t*height), int(r*width), int(b*height)))
        # Bypass generic trim logic below since it's manual
        return cropped

    # Generic crop and trim
    cropped = img.crop((0, max(0, final_top - 15), width, min(height, final_bottom + 15)))
    bg = Image.new(cropped.mode, cropped.size, (255, 255, 255))
    diff = ImageChops.difference(cropped, bg)
    bbox = diff.getbbox()
    if bbox:
        p = 5
        bbox = (max(0, bbox[0]-p), max(0, bbox[1]-p), 
                min(cropped.size[0], bbox[2]+p), min(cropped.size[1], bbox[3]+p))
        cropped = cropped.crop(bbox)
    return cropped

def img_to_b64(img, format="PNG"):
    buffered = BytesIO()
    img.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode()
