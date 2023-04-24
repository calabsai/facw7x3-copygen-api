# anthropic_handler.py, Path: backend/app/src/anthropic_handler.py

import requests

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/complete"

def generate_copy(system_role_prompt, context, prompt, model="claude-v1.3", api_key=None):
    headers = {
        "x-api-key": api_key,  # Use the passed API key
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"{system_role_prompt}\n{context}\n{prompt}",
        "model": model,
        "max_tokens_to_sample": 1024,
        "stop_sequences": ["\n\nHuman:"],
        "temperature": 0.8
    }

    try:
        response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
        response_json = response.json()
        generated_response = response_json["completion"]
        return generated_response.strip()
    except Exception as e:
        print(f"Error generating copy: {e}")
        return "Error generating copy"