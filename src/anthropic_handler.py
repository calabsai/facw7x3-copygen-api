# anthropic_handler.py, Path: facw7x3-copygen-api/src/anthropic_handler.py

import requests
from tenacity import retry, stop_after_attempt, wait_random_exponential

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/complete"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def make_api_call(headers, data):
    return requests.post(ANTHROPIC_API_URL, headers=headers, json=data)

def generate_copy(system_role_prompt, context, prompt, model="claude-v1.3", anthropic_api_key=None):  
    headers = {  
        "x-api-key": anthropic_api_key, # Use the passed API key  
        "Content-Type": "application/json"  
    }  
    data = {  
        "prompt": f"{system_role_prompt}\n{context}\n{prompt}",  
        "model": model,  
        "max_tokens_to_sample": 2048,  
        "stop_sequences": ["\n\nHuman:"],  
        "temperature": 0.8  
    }

    # Print the input data for debugging
    print(f"Input data for Anthropic API:")
    print(f"  System Role Prompt: {system_role_prompt}")
    print(f"  Context: {context}")
    print(f"  Prompt: {prompt}")
    print(f"  Model: {model}")

    try:
        response = make_api_call(headers, data)
        response_json = response.json()
        # Print the full API response for debugging
        print(f"API response JSON: {response_json}")
        generated_response = response_json.get("completion", "")  # Use .get() to handle missing keys
        if not generated_response:
            print("Generated response is empty.")  # Print a message if the response is empty
        return generated_response.strip()
    except Exception as e:
        print(f"Error generating copy: {e}")
        return "Error generating copy"
