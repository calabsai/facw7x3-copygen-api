# openai_gpt_3_5_t_handler.py, Path: backend/app/src/openai_gpt_3_5_t_handler.py

import openai
import time
import datetime

def generate_copy_with_retry(data, max_retries=3, delay_factor=2):
    retries = 0
    response = None

    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(**data)
            break
        except openai.error.RateLimitError as e:
            if retries < max_retries - 1:
                sleep_time = delay_factor * (2 ** retries)
                print(f"RateLimitError encountered. Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
                retries += 1
            else:
                print("Max retries reached. Aborting.")
                raise e
    return response

def generate_copy(system_role_prompt, context, prompt, model="gpt-3.5-turbo", openai_api_key=None):
    # Set the OpenAI API key
    openai.api_key = openai_api_key

    data = {
        "model": model,  # Use the selected model
        "messages": [
            {"role": "system", "content": system_role_prompt},
            {"role": "user", "content": context},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1024,
        "n": 1,
        "temperature": 0.8,
    }

    try:
        response = generate_copy_with_retry(data)
        if response and response.choices:
            generated_response = response.choices[0].message["content"]
            return generated_response.strip()
        return "Error generating copy"
    except Exception as e:
        print(f"Error generating copy: {e}")
        import traceback
        traceback.print_exc()
        return "Error generating copy"
