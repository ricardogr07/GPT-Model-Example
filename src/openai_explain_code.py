import openai
import tkinter as tk
from tkinter import simpledialog
from openai_handler import OpenAIApiHandler

class CodeExplain(OpenAIApiHandler):
    def __init__(self):
        super().__init__()

    def format_user_prompt(self, code_block: str) -> str:
        """Format user code input for API."""
        lines = code_block.strip().split("\n")
        code_content = lines[1:-1]
        formatted_code = "\\n".join(line.replace("\n", "").replace("\"", "\\\"") for line in code_content)
        return f"```{formatted_code}\\n```"

    def request_code_explanation(self, code_to_explain: str) -> str:
        """Request code explanation using OpenAI API."""
        formattedPrompt = self.format_user_prompt(code_to_explain)

        messages = [
            {
                "role": "system",
                "content": "You are a senior software developer who does not like code smells or bad coding practices. You will be helping a junior software engineer who is a fresh graduate and presents you with code that they do not entirely understand. For each piece of code I give you, explain it, and give me a revised version with comments.\n\nI will give you the next input for each code that I need to be explained:\n```{coding_language}\n{code}\n```\nI expect you to give me your answer in the following format:\n\"Here is\" + {one liner explaining the code} + \":\"\n```{coding_language}\n{code with added comments to explain it better}\n```\nStep by step explanation: {step by step explanation of the code}\n{summary of what does the code do}"
            },
            {
                "role": "user",
                "content": formattedPrompt
            }
        ]

        return self.generate_chat_completion(messages)
