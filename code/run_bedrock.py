import litellm
import json
import argparse
import os
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

 
VERTEX_AI_CREDENTIAL = ""

def query_litellm(prompt, llm_model, temperature):

    try:
        response = litellm.completion(
            model=llm_model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You must LIMIT YOUR RESPONSE TO 130 TOKENS.",
                },
                {"role": "user", "content": prompt},
            ],
            vertex_credentials=VERTEX_AI_CREDENTIAL,
        )
        return response
    except Exception as e:
        print(f"An error occurred during API query: {e}")
    return None


def extract_response_content(response):

    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, TypeError) as e:
        print(f"Error extracting response content: {e}")
        print("Full response:", response)
    return None


def read_prompt_from_file(file_path):

    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return None


def save_responses_to_json(responses, folder_path, model, temperature, trial):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

 
    sanitized_model = model.replace("bedrock/", "")

    output_file_name = f"output_responses_{sanitized_model}_temp{temperature}_{timestamp}_trial_{trial}.json"
    output_file_path = os.path.join(folder_path, output_file_name)
    try:
        with open(output_file_path, 'w') as file:
            json.dump(responses, file, indent=4)
        print(f"Responses saved to {output_file_path}")
    except Exception as e:
        print(f"Failed to save the file: {e}")


def process_file(filename, folder_path, model, temperature):

    match = re.match(r'output_sample_(\d+)\.txt', filename)
    if match:
        num = int(match.group(1))
        if num <= 500:
            file_path = os.path.join(folder_path, filename)
            prompt_text = read_prompt_from_file(file_path)
            if prompt_text:
                print(f"Processing file: {filename}")
                response = query_litellm(prompt_text, model, temperature)
                content = extract_response_content(response)
                return filename, content
    return filename, None


def process_folder_parallel(folder_path, model, temperature, trial, max_workers=10):

    responses = {}
    files = [f for f in os.listdir(folder_path) if re.match(r'output_sample_(\d+)\.txt', f)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_file, file, folder_path, model, temperature): file for file in files}

        for future in as_completed(future_to_file):
            filename, content = future.result()
            if content:
                responses[filename] = content

    save_responses_to_json(responses, folder_path, model, temperature, trial)

     
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process all text files in a given folder for AI analysis.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing prompt files.")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for querying the API.")
    parser.add_argument("--temperature", type=float, default=0.5, help="Temperature setting for the AI model.")
    parser.add_argument("--trial", type=str, default=0, help="Trial setting for the AI model.")
 
    args = parser.parse_args()

    prompt_text = "Hello, what model are you? What am i working with?"
 
    model = 'bedrock/us.meta.llama3-1-70b-instruct-v1:0'
    temperature = 0.7
    response = query_litellm(prompt_text, model, temperature)
    content = extract_response_content(response)
    print(content)

    print("In run_api.py, running", args)

    process_folder_parallel(args.folder_path, args.model, args.temperature, args.trial)