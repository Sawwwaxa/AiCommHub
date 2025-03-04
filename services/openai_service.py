import os
import logging
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)

def process_message(text: str) -> str:
    """
    Process a message using OpenAI API

    Args:
        text: The input text to process

    Returns:
        str: The processed response or an error message
    """
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            return "Configuration error: OpenAI API key not set"

        # Initialize client only when needed
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Sorry, I couldn't process your message at this time."