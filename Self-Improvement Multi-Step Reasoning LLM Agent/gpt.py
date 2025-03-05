import openai
import logging
from config import OPENAI_API_KEY, FINE_TUNED_MODEL

# Setup OpenAI API key
openai.api_key = OPENAI_API_KEY


def gpt_call(prompt, temperature=0.7, model=FINE_TUNED_MODEL):
    """
    Calls the OpenAI API using the specified model.
    """
    logging.info(f"[LLM PROMPT]: {prompt.strip()[:300]}...")
   
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        result = response["choices"][0]["message"]["content"].strip()
        logging.info(f"[LLM RESPONSE]: {result.strip()[:300]}...")
        return result
    except Exception as e:
        logging.error(f"[OpenAI API Error]: {str(e)}")
        return f"Error: {str(e)}"