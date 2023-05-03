# openai_gpt_3_5_t_handler.py, Path: facw7x3-copygen-api/src/openai_gpt_3_5_t_handler.py
import openai
import datetime
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def generate_copy_with_retry(data):
    return openai.ChatCompletion.create(**data)

def generate_copy(system_role_prompt, context, prompt, model="gpt-3.5-turbo", openai_api_key=None):
    # Set the OpenAI API key
    openai.api_key = openai_api_key

    data = {
        "model": model,
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
        return f"Error generating copy: {str(e)}"