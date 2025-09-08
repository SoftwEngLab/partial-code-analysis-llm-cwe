import json
import os
import sys

def read_template_file(template_file_path):
    with open(template_file_path, 'r') as file:
        return file.read()

def process_jsonl_file(file_path, output_directory, content_template, func_src_key):
    with open(file_path, 'r') as file:
        for i, line in enumerate(file, start=1):
            entry = json.loads(line)
            func_src = entry.get(func_src_key)
            if func_src is None:
                continue
            final_text = content_template.replace("{func_src_x}", func_src)
            output_file_name = f'output_sample_{i}.txt'
            output_file_path = os.path.join(output_directory, output_file_name)
            with open(output_file_path, 'w') as output_file:
                output_file.write(final_text)
            print(f'Sample {i} processed and saved as {output_file_path}.')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: script.py <jsonl_file_path> <template_file_path> <experiment_file_path> <func_src_before/after>")
        sys.exit(1)

    jsonl_file_path = sys.argv[1]
    template_file_path = sys.argv[2]
    experiment_file_path = sys.argv[3]
    func_src_key = sys.argv[4] 
    print(sys.argv) 
    output_dir_base = os.path.splitext(experiment_file_path)[0]
    output_directory = f'{output_dir_base}/{func_src_key}'

    os.makedirs(output_directory, exist_ok=True)

    content_template = read_template_file(template_file_path)

    process_jsonl_file(jsonl_file_path, output_directory, content_template, func_src_key)
