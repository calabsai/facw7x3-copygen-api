# openai_handler_async.py, Path: backend/app/src/openai_handler_async.py

import openai
import time
import logging
import asyncio
import aiohttp
from functools import lru_cache

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@lru_cache(maxsize=100)
async def generate_copy_cached(system_role_prompt, context, prompt, model="gpt-4", openai_api_key=None, max_retries=3, delay_factor=2):
    async with aiohttp.ClientSession() as session:
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

        async def make_api_call():
            headers = {"Authorization": f"Bearer {openai_api_key}"}
            async with session.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers) as resp:
                return await resp.json()

        retries = 0
        response = None

        while retries < max_retries:
            try:
                response = await make_api_call()
                break
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if retries < max_retries - 1:
                    sleep_time = delay_factor * (2 ** retries)
                    logger.info(f"Error encountered: {e}. Retrying in {sleep_time} seconds...")
                    await asyncio.sleep(sleep_time)
                    retries += 1
                else:
                    logger.error("Max retries reached. Aborting.")
                    raise e

        if response and response["choices"]:
            generated_response = response["choices"][0]["message"]["content"]
            return generated_response.strip()

        return "Error generating copy"

async def generate_copy(system_role_prompt, context, prompt, model="gpt-4", openai_api_key=None, max_retries=3, delay_factor=2):
    return await generate_copy_cached(system_role_prompt, context, prompt, model=model, openai_api_key=openai_api_key, max_retries=max_retries, delay_factor=delay_factor)