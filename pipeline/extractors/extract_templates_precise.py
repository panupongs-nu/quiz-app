import numpy as np
from PIL import Image
import os

def extract_precise_templates():
    # Load page 3 which has clear Q1 and a)
    img = Image.open("pages/page-03.jpg").convert('L')
    img_np = np.array(img)
    
    # Q1. is near (95, 90)
    # Let's crop a slightly larger area and find the character
    q_zone = img_np[80:110, 80:120]
    # Threshold to find the 'Q'
    q_char = (q_zone < 128).astype(np.uint8) * 255
    # Find bounding box of the black pixels
    coords = np.argwhere(q_char == 255)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    q_template = Image.fromarray(q_zone[y0:y1+1, x0:x1+1])
    q_template.save("template_Q.png")
    
    # a) is near (95, 195)
    a_zone = img_np[185:215, 80:120]
    a_char = (a_zone < 128).astype(np.uint8) * 255
    coords = np.argwhere(a_char == 255)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    a_template = Image.fromarray(a_zone[y0:y1+1, x0:x1+1])
    a_template.save("template_a.png")
    
    print(f"Extracted Q template: {q_template.size}")
    print(f"Extracted a) template: {a_template.size}")

if __name__ == "__main__":
    extract_precise_templates()
