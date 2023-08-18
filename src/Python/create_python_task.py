import os
from datetime import datetime
import argparse
from handlers.openai_python_creation import PythonCodeCreation
from handlers.openai_explain_code import CodeExplain

class PythonTaskCreator:
    def __init__(self):
        self.python_code_creator = PythonCodeCreation()
        self.code_explanations = CodeExplain()

    def process_prompt(self, prompt):
        natural_language_query, answer_query = self.python_code_creator.separate_prompt_and_answer(prompt)
        answer = self.code_explanations.request_code_explanation(answer_query)    
        return natural_language_query, answer
    
    def run(self, task_id):
        example = self.python_code_creator.request_new_example()
        prompt1, prompt2, prompt3, prompt4, prompt5 = self.python_code_creator.extract_prompts_and_answers(example)
        prompts = [prompt1, prompt2, prompt3, prompt4, prompt5]

        # Get today's date in the format YYYY-MM-DD
        today_date = datetime.today().strftime('%Y-%m-%d')
        # Create the directory with the specified date if it doesn't exist
        if not os.path.exists(today_date):
            os.makedirs(today_date)

        # Define the file path
        file_path = os.path.join(today_date, f'{task_id}.txt')

        with open(file_path, 'w') as file:
           
            for i, prompt in enumerate(prompts, 1):
                prompt, answer = self.process_prompt(prompt)
                file.write(f"\n\nPrompt {i}:\n")
                file.write(prompt)
                file.write(f"\n\nAnswer {i}:\n")
                file.write(answer)

        # Open the .txt file automatically
        os.system(f'start notepad {file_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Python Task')
    parser.add_argument('taskID', type=str, help='Task ID for this run')
    args = parser.parse_args()  
    handler = PythonTaskCreator()
    handler.run(args.taskID)
