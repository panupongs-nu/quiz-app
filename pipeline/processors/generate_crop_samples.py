import os
from PIL import Image
from image_utils import smart_crop

def generate_samples():
    output_dir = "crop_samples"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Selecting a diverse range of questions to test the algorithm
    samples = [
        {"id": "2025A-Q-013", "path": "pages/page-07.jpg"}, # IoT Architecture
        {"id": "2025A-Q-041", "path": "pages/page-18.jpg"}, # Security table
        {"id": "2025A-Q-064", "path": "pages/page-26.jpg"}, # Governance Roles Table
        {"id": "2025A-Q-092", "path": "pages/page-34.jpg"}, # Engineering Flowchart
        {"id": "2025S-Q-030", "path": "images/2025S_IP/page-15.png"} # Network Firewall Diagram
    ]
    
    for s in samples:
        if os.path.exists(s["path"]):
            with Image.open(s["path"]) as img:
                cropped = smart_crop(img, s["id"])
                out_path = os.path.join(output_dir, f"sample_{s['id']}.png")
                cropped.save(out_path)
                print(f"Saved sample: {out_path}")
        else:
            print(f"Source not found: {s['path']}")

if __name__ == "__main__":
    generate_samples()
