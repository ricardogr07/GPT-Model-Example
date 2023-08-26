import os
from datetime import datetime
import argparse
from handlers.openai_sql_creation import SQLCodeCreation
from handlers.openai_explain_code import CodeExplain

class TaskCreator:
    def __init__(self, specifications):
        self.specifications = specifications
        self.sql_code_creator = SQLCodeCreation(self.specifications)
        self.code_explanations = CodeExplain()

    def process_prompt(self, query):
        natural_language_query, answer_query = self.sql_code_creator.extract_query_components(query)
        answer = self.code_explanations.request_code_explanation(answer_query)    
        return natural_language_query, answer
    
    def run(self, task_id):
        example = self.sql_code_creator.request_new_example()
        tables_section, query1, query2, query3, query4, query5 = self.sql_code_creator.split_input_into_sections(example)
        queries = [query1, query2, query3, query4, query5]

        # Get today's date in the format YYYY-MM-DD
        today_date = datetime.today().strftime('%Y-%m-%d')
        # Create the directory with the specified date if it doesn't exist
        if not os.path.exists(today_date):
            os.makedirs(today_date)

        # Define the file path
        file_path = os.path.join(today_date, f'{task_id}.txt')

        with open(file_path, 'w') as file:
            file.write("Tables:\n")
            file.write(tables_section)
            
            for i, query in enumerate(queries, 1):
                if i == 1:
                    # Special handling for the first query
                    prompt, answer = self.process_prompt(query)
                    tables_and_first_query = tables_section + "\n" + prompt
                    firstPrompt = self.sql_code_creator.format_first_prompt(tables_and_first_query)                    
                    file.write(f"\n\nPrompt {i}:\n")
                    file.write(firstPrompt)
                    file.write(f"\n\nAnswer {i}:\n")
                    file.write(answer)
                else:
                    # Handling for the rest of the queries
                    prompt, answer = self.process_prompt(query)
                    file.write(f"\n\nPrompt {i}:\n")
                    file.write(prompt)
                    file.write(f"\n\nAnswer {i}:\n")
                    file.write(answer)


        # Open the .txt file automatically
        os.system(f'start notepad {file_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate SQL Task')
    parser.add_argument('taskID', type=str, help='Task ID for this run')
    parser.add_argument('specifications', type=str, nargs='?', default='', help='Any specifics about the task')
    args = parser.parse_args()  
    handler = TaskCreator(args.specifications)
    handler.run(args.taskID)
