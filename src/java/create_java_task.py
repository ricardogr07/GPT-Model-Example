import os
from datetime import datetime
import argparse
import logging
from handlers.openai_java_creation import JavaCodeCreation
from handlers.create_task import TaskCreator
import subprocess

logging.basicConfig(filename='java_error_log.txt', level=logging.ERROR)


class JavaTaskCreator(TaskCreator):
    def __init__(self, code_creator_type=JavaCodeCreation):
        super().__init__(code_creator_type)

    def process_prompt(self, prompt_and_answer):
        # Unpacking the tuple into two separate variables
        natural_language_query, answer_query = prompt_and_answer       
        # Further processing using the unpacked variables
        answer = self.code_explanations.request_code_explanation(answer_query)    
        return natural_language_query, answer

    def save_to_file(self, prompts, task_id):
        today_date = datetime.today().strftime('%Y-%m-%d')
        if not os.path.exists(today_date):
            os.makedirs(today_date)
        file_path = os.path.join(today_date, f'{task_id}.txt')

        with open(file_path, 'w') as file:
            for i, prompt in enumerate(prompts, 1):
                prompt_text, answer_text = self.process_prompt(prompt)
                file_content = f"\n\nPrompt {i}:\n{prompt_text}\n\nAnswer {i}:\n{answer_text}"
                file.write(file_content)

        return file_path

    def process_task(self, task_id):
        try:
            new_example = self.code_creator.request_new_example()
            prompts = self.code_creator.extract_prompts_and_answers(new_example)
            file_path = self.save_to_file(prompts, task_id)
            subprocess.run(['notepad', file_path])

        except FileNotFoundError:
            logging.error("Error processing task: File not found.", exc_info=True)
            raise
        except PermissionError:
            logging.error("Error processing task: Permission error.", exc_info=True)
            raise
        except ValueError:
            logging.error("Error processing task: Value error encountered.", exc_info=True)
            raise
        except Exception as e:
            logging.error(f"Error processing task: {str(e)}", exc_info=True)
            raise        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Java Task')
    parser.add_argument('taskID', type=str, help='Task ID for this run')
    args = parser.parse_args()  
    handler = JavaTaskCreator()
    handler.process_task(args.taskID)
