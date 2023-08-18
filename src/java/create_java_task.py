import os
from datetime import datetime
import argparse
from handlers.openai_java_creation import JavaCodeCreation
from handlers.openai_explain_code import CodeExplain

class JavaTaskCreator:
    def __init__(self):
        self.java_code_creator = JavaCodeCreation()
        self.code_explanations = CodeExplain()

    def process_prompt(self, prompt_and_answer):
        # Unpacking the tuple into two separate variables
        natural_language_query, answer_query = prompt_and_answer       
        # Further processing using the unpacked variables
        answer = self.code_explanations.request_code_explanation(answer_query)    
        return natural_language_query, answer

    def run(self, task_id):
        example = self.java_code_creator.request_new_example()
        prompts_and_answers = self.java_code_creator.extract_prompts_and_answers(example)
        # Get today's date in the format YYYY-MM-DD
        today_date = datetime.today().strftime('%Y-%m-%d')
        # Create the directory with the specified date if it doesn't exist
        if not os.path.exists(today_date):
            os.makedirs(today_date)

        # Define the file path
        file_path = os.path.join(today_date, f'{task_id}.txt')

        with open(file_path, 'w') as file:
           
            for i, prompt in enumerate(prompts_and_answers, 1):
                prompt, answer = self.process_prompt(prompts_and_answers[i-1])
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
    handler = JavaTaskCreator()
    handler.run(args.taskID)
