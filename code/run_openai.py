import openai
import json
import argparse
import os
import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI



def query_openai(prompt, model, temperature, mode):
    """
    Queries the OpenAI API or Hugging Face API depending on the mode.
    """
    try:
        if mode == "deepseek":
            client = OpenAI(
                base_url="https://huggingface.co/api/inference-proxy/together",
                api_key=""
            )
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Limit your response to 130 tokens."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stream=False
            )
            return response
        elif mode == "hf_endpoint":
            return query_hf_api(prompt, temperature)
        elif mode == "o1":
            print("......", mode)
            client = openai
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Limit your response to 500 tokens."},
                    {"role": "user", "content": prompt},
                ])
            return response
        else:
            client = openai
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Limit your response to 130 tokens."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stream=False
            )
            return response
        
    except Exception as e:
        print(f"An error occurred during API query: {e}")
    return None

def query_hf_api(prompt, temperature):
    """
    Queries the Hugging Face API.
    """
 
    try:
        client = OpenAI(
            base_url="https://ue4xb2y39sfo803n.us-east-1.aws.endpoints.huggingface.cloud/v1/", 
            api_key="" 
            )
        
        response = client.chat.completions.create(
            model="tgi",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant. Limit your response to 130 tokens."},
                    {"role": "user", "content": prompt},
                ],
            top_p=None,
            temperature=None,
            max_tokens=150,
            stream=False,
            seed=None,
            stop=None,
            frequency_penalty=None,
            presence_penalty=None
            )
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while querying the Hugging Face API: {e}")
    return None

def extract_response_content(response, mode):
    """
    Extracts the content from the API response for serialization.
    """
    try:
        if mode == "hf_endpoint_wrong":
            if isinstance(response, list) and len(response) > 0:
                response = response[0] 
            return response.get("generated_text", "")
        else:
            print("......", response)
            return response.choices[0].message.content
    except (KeyError, TypeError) as e:
        print(f"Error extracting response content: {e}")
        print("Full response:", response)
    return None

def read_prompt_from_file(file_path):
    """
    Reads the prompt from a file.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return None

def save_responses_to_json(responses, folder_path, model, temperature, trial):
    """
    Saves all responses to a single JSON file.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_name = f"output_responses_{model.replace('/', '_')}_temp{temperature}_{timestamp}_trial_{trial}.json"
    output_file_path = os.path.join(folder_path, output_file_name)
    try:
        with open(output_file_path, 'w') as file:
            json.dump(responses, file, indent=4)
        print(f"Responses saved to {output_file_path}")
    except Exception as e:
        print(f"Failed to save the file: {e}")

def process_file(filename, folder_path, model, temperature, mode):
    """
    Processes a single file.
    """
    match = re.match(r'output_sample_(\d+)\.txt', filename)
    if match:
        num = int(match.group(1))
        if num <= 500:
            file_path = os.path.join(folder_path, filename)
            prompt_text = read_prompt_from_file(file_path)
            if prompt_text:
                print(f"Processing file: {filename}")
                response = query_openai(prompt_text, model, temperature, mode)
                print("--------------------", response)
                content = extract_response_content(response, mode)
                return filename, content
    return filename, None

def process_folder_parallel(folder_path, model, temperature, trial, mode, max_workers=10):

    responses = {}
    files = [f for f in os.listdir(folder_path) if re.match(r'output_sample_(\d+)\.txt', f)]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_file, file, folder_path, model, temperature, mode): file for file in files}
        for future in as_completed(future_to_file):
            filename, content = future.result()
            if content:
                responses[filename] = content
    save_responses_to_json(responses, folder_path, model, temperature, trial)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process text files for AI analysis.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing prompt files.")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for querying the API.")
    parser.add_argument("--temperature", type=float, default=0.5, help="Temperature setting for the AI model.")
    parser.add_argument("--trial", type=str, default="0", help="Trial setting.")
    args = parser.parse_args()

    mw = 10
    mode = "openai"
    if args.model == "deepseek-ai/DeepSeek-R1":
        mode = "deepseek"
    elif args.model == "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B":
        mode = "hf_endpoint"
        mw = 1
    elif args.model == "o1":
        mode = "o1"
        mw = 1

    process_folder_parallel(args.folder_path, args.model, args.temperature, args.trial, mode, max_workers=mw)
