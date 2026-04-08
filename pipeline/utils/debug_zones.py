from PIL import Image
import os

def debug_zones():
    img = Image.open("pages/page-03.jpg")
    # Save a large chunk of top left to see where we are
    debug_crop = img.crop((0, 0, 300, 300))
    debug_crop.save("debug_top_left.png")
    print("Saved debug_top_left.png")

if __name__ == "__main__":
    debug_zones()
