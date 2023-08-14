# code_explain.py

import openai
import tkinter as tk
from tkinter import simpledialog
from openai_handler import OpenAIApiHandler

class CodeExplain(OpenAIApiHandler):
    def __init__(self):
        super().__init__()  # Call parent constructor

    def get_multiline_input(self):
        """Get multiline input using a GUI dialog."""
        tk.Tk().withdraw()  # Hide main window
        return simpledialog.askstring("Input", "Please paste your code:")

    def format_user_prompt(self, code_block: str, language: str) -> str:
        """Format user code input for API."""
        lines = code_block.strip().split("\n")
        code_content = lines[1:-1]
        formatted_code = "\\n".join(line.replace("\n", "").replace("\"", "\\\"") for line in code_content)
        return f"```{language}{formatted_code}\\n```"

    def request_code_explanation(self):
        """Request code explanation using OpenAI API."""
        language = input("Define the language:")
        prompt = self.get_multiline_input()
        formattedPrompt = self.format_user_prompt(prompt, language.lower())

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
            print(response['choices'][0]['message']['content'])
        except openai.error.OpenAIError as e:  # Be specific with the exception
            print(f"Error during API call: {e}")


if __name__ == "__main__":
    explainer = CodeExplain()
    explainer.request_code_explanation()
