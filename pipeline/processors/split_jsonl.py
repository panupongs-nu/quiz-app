import os
import json

def split_file(file_path, chunk_size=20):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    base_name = os.path.splitext(file_path)[0]
    output_dir = f"{base_name}_splits"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        chunk_num = (i // chunk_size) + 1
        output_file = os.path.join(output_dir, f"{base_name}_part{chunk_num:02d}.jsonl")
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.writelines(chunk)
        print(f"Created {output_file}")

if __name__ == "__main__":
    split_file('2025A_IP_Questions.jsonl')
    split_file('2025S_IP_Questions.jsonl')
