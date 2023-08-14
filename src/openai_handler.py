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