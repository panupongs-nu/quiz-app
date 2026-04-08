import opendataloader_pdf
import os
import json

def test_opendataloader():
    input_file = "itpec_exams/2025A_IP_Questions.pdf"
    output_dir = "opendataloader_test"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Converting {input_file} to JSON...")
    # Convert only a small range to save time/resources
    # This tool usually supports range but let's check basic convert first
    # Many PDF tools process all, let's try a single page if possible
    # Actually, the docs say it takes a list of paths.
    
    # We might want to use the CLI to test a page range if the SDK is opaque
    # But let's try the Python way.
    try:
        opendataloader_pdf.convert(
            input_path=[input_file],
            output_dir=output_dir,
            format="json"
        )
        print("Conversion complete.")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    test_opendataloader()
