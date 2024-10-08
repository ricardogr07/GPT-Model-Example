import os
from datetime import datetime
import argparse
import logging
from handlers.openai_python_creation import PythonCodeCreation
from handlers.create_task import TaskCreator
from handlers.enums import Project
import subprocess

logging.basicConfig(filename='python_error_log.txt', level=logging.ERROR)

class PythonTaskCreator(TaskCreator):
    def __init__(self, code_creator_type=PythonCodeCreation):
        super().__init__(code_creator_type)

    def save_to_file(self, prompts, task_id, project: Project):
        today_date = datetime.today().strftime('%Y-%m-%d')
        if not os.path.exists(today_date):
            os.makedirs(today_date)
        file_path = os.path.join(today_date, f'{task_id}.txt')

        with open(file_path, 'w') as file:
            for i, prompt in enumerate(prompts, 1):
                if project == Project.FANCY_RAT:
                    prompt_text, answer_text = super().process_prompt(prompt)
                else:
                    prompt_text, answer_text = super().process_prompt_with_driver_code(prompt)
                file_content = f"\n\nPrompt {i}:\n{prompt_text}\n\nAnswer {i}:\n{answer_text}"
                file.write(file_content)

        return file_path

    def process_task(self, task_id, project):
        try:
            new_example = self.code_creator.request_new_example()
            prompts = self.code_creator.extract_prompts_and_answers(new_example)           
            file_path = self.save_to_file(prompts, task_id, project)
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
    parser = argparse.ArgumentParser(description='Generate Python Task')
    parser.add_argument('taskID', type=str, help='Task ID for this run')
    parser.add_argument('project', type=str, help='Project being used for this run')
    args = parser.parse_args() 
    try:
        project= Project[args.project]
    except KeyError:
        logging.error("Error processing task: Invalid project name.", exc_info=True)
        raise
    handler = PythonTaskCreator()
    handler.process_task(args.taskID, project)
    