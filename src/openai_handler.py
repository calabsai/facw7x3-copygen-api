# openai_handler.py, Path: facw7x3-copygen-api/src/openai_handler.py
import openai
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def generate_copy_with_retry(data):
    return openai.ChatCompletion.create(**data)

def generate_copy(system_role_prompt, context, prompt, model="gpt-4", openai_api_key=None, max_retries=3, delay_factor=2):
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
        logger.error(f"Error generating copy: {e}")
        return f"Error generating copy: {str(e)}"