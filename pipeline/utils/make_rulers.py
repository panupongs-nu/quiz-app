from PIL import Image, ImageDraw
import os

def create_ruler(image_path, output_name):
    if not os.path.exists(image_path):
        print(f"Not found: {image_path}")
        return
        
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    for i in range(1, 20): # 5% increments
        y = int(height * (i * 0.05))
        draw.line([(0, y), (width, y)], fill="red", width=5)
        # Using default font, so we'll draw a rect background to see it
        draw.rectangle([(0, y-10), (40, y+10)], fill="white")
        draw.text((5, y-5), f"{i*5}%", fill="red")
        
    img.save(output_name)

create_ruler("pages/page-07.jpg", "ruler_page07.jpg")
create_ruler("pages/page-18.jpg", "ruler_page18.jpg")
create_ruler("pages/page-26.jpg", "ruler_page26.jpg")
create_ruler("pages/page-34.jpg", "ruler_page34.jpg")
create_ruler("images/2025S_IP/page-15.png", "ruler_s_page15.png")
