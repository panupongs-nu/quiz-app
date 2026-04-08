import os
import json
import argparse

def split_file(file_path, chunk_size=20):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Extract just the filename without extension for directory/prefix naming
    base_file_name = os.path.basename(file_path)
    file_stem = os.path.splitext(base_file_name)[0]
    
    # Create the output directory in the same place as the input file
    output_dir = os.path.join(os.path.dirname(file_path), f"{file_stem}_splits")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_chunks = (len(lines) + chunk_size - 1) // chunk_size
    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        chunk_num = (i // chunk_size) + 1
        output_file_name = f"{file_stem}_part{chunk_num:02d}.jsonl"
        output_file_path = os.path.join(output_dir, output_file_name)
        
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            f_out.writelines(chunk)
            
    print(f"Split {file_path} into {total_chunks} parts in {output_dir}")

if __name__ == "__main__":
    files_to_split = [
        "data/processed_jsonl/2025S_IP_Questions.jsonl",
        "data/processed_jsonl/2024A_IP_Questions.jsonl",
        "data/processed_jsonl/2024S_IP_Questions.jsonl"
    ]
    for f in files_to_split:
        split_file(f)
