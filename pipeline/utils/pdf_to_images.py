import os
import sys
from pdf2image import convert_from_path

def convert_pdf(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Converting {pdf_path} to images in {output_dir}...")
    images = convert_from_path(pdf_path, dpi=300)
    
    for i, image in enumerate(images):
        page_num = i + 1
        output_file = os.path.join(output_dir, f"page-{page_num:02d}.jpg")
        image.save(output_file, "JPEG", quality=90)
        if page_num % 10 == 0:
            print(f"Processed {page_num} pages...")
            
    print(f"Conversion complete. Total pages: {len(images)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pdf_to_images.py <pdf_path> <output_dir>")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    convert_pdf(pdf_path, output_dir)
