import json
import openai
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from together import Together
import re

def query_openai(client, prompt, model, temperature, max_tokens, mode):
    """
    Queries the OpenAI API with the specified parameters and returns the response.
    """
    try:
        if mode == "o1":
            client = openai
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Limit your response to 500 tokens."},
                    {"role": "user", "content": prompt},
                ])
            return response
        elif mode == "o1-mini":
            client = openai
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt},
                ])
            return response
        elif mode == "together":
            os.environ['TOGETHER_API_KEY'] = ''
            client = Together()
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Limit your response to 130 tokens."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                top_p=1,
                seed=42
            )
 
            return response
        else:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stream=False
            )
            return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def determine_vulnerability(response):
    prompt = f"Determine if the following response indicates a vulnerability was found:\n\n{response}\n\nRespond ONLY with 'vulnerable' or 'non-vulnerable'. Answer in this format: ['response': 'vulnerable'] or  ['response': 'non-vulnerable']"
    completion = query_openai(
        client=openai,
        prompt=prompt,
        model= "o1-mini",#"deepseek-ai/DeepSeek-R1",
        temperature=1.0,
        max_tokens=4096,
        mode = "o1-mini"
    )

    if completion is not None:
 
        content = completion.choices[0].message.content.strip().lower()
 
        if "['response': 'vulnerable']" in content:
            result = "vulnerable"
        elif "['response': 'non-vulnerable']" in content:
            result = "non-vulnerable"
        else:
            result = "inconclusive"
        return result
    else:
 
        return "ERROR"



def process_json(input_file, output_file, max_workers=10):
    """
    Processes a JSON file in a multithreaded manner.
    
    :param input_file: Path to input JSON file
    :param output_file: Path to save output JSON results
    :param max_workers: Number of threads for concurrent processing
    """
    with open(input_file, 'r') as f:
        data = json.load(f)

    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_key = {executor.submit(determine_vulnerability, response): key for key, response in data.items()}

        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as e:
                print(f"Error processing {key}: {e}")
                results[key] = "ERROR"

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_json_file> <output_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

 
    process_json(input_file, output_file, max_workers=100)
