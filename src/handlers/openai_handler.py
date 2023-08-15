import logging
import os
import openai
from dotenv import load_dotenv

class OpenAIApiHandler:
    def __init__(self):
        self.configure_openai()

    def configure_openai(self):
        """Set up OpenAI configurations."""
        load_dotenv()
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        self.OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE')

        openai.api_type = "azure"
        openai.api_key = self.OPENAI_API_KEY
        openai.api_base = self.OPENAI_API_BASE
        openai.api_version = "2023-03-15-preview"

    def generate_chat_completion(self, messages: list) -> str:
        """
        Generate chat completion using OpenAI API.

        :param messages: The messages array to pass to the API
        :return: The content from the response or an error message
        """
        try:
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=messages,
                temperature=0,
                max_tokens=4000,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            return response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            logging.error(f"Error during API call: {e}")
            raise
