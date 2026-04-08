from PIL import Image
import os

def extract_templates():
    # Load a representative page
    img = Image.open("pages/page-03.jpg").convert('L')
    
    # Coordinates for 'Q' in Q1. (manual estimation from previous turns and image)
    # Let's try to be precise. Top left of Q1 is roughly at y=100
    # On a standard 72/96dpi image, but let's look at the full image provided.
    # The image is roughly 1000px wide.
    # Q1 is near top left.
    
    # Q template (approximate box around 'Q')
    q_template = img.crop((85, 80, 115, 110))
    q_template.save("q_anchor_template.png")
    
    # 'a)' template (approximate box around 'a)')
    a_template = img.crop((85, 185, 115, 215))
    a_template.save("a_anchor_template.png")
    
    print("Templates saved.")

if __name__ == "__main__":
    extract_templates()
