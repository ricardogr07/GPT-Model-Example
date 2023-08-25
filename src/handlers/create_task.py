from abc import ABC, abstractmethod
from handlers.openai_python_creation import PythonCodeCreation
from handlers.openai_handler import OpenAIApiHandler as AIHandler
from handlers.openai_explain_code import CodeExplain

class TaskCreator(ABC):

    def __init__(self, code_creator_type):
        if not issubclass(code_creator_type, AIHandler):
            raise ValueError("code_creator_type must be an instance or subclass of OpenAIApiHandler")
        self.code_creator = code_creator_type()
        self.code_explanations = CodeExplain()
    
    def process_prompt(self, prompt):
        natural_language_query, answer_query = self.code_creator.separate_prompt_and_answer(prompt)
        answer = self.code_explanations.request_code_explanation(answer_query)
        return natural_language_query, answer

    @abstractmethod
    def process_task(self, prompt):
        pass  
