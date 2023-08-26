from handlers.openai_handler import OpenAIApiHandler as AIHandler
import re
import json
import random
import os

class PythonCodeCreation(AIHandler):
    def __init__(self):
        super().__init__()     

    def separate_prompt_and_answer(self, text):
        # Split the section into prompt and answer using '\nAnswer ' as a delimiter
        prompt, answer = text.split('\nAnswer ')
        # Clean up the prompt and answer by stripping leading/trailing whitespaces
        prompt = prompt.strip().replace('Prompt ', '').replace(
            'Input:\nNext\nOutput:\n', '')
        # Remove the index (like "5:") from the start of the prompt text
        prompt = ':'.join(prompt.split(':')[1:]).strip()
        answer = ':'.join(answer.split(':')[1:]).strip()
        return prompt, answer

    def extract_prompts_and_answers(self,s):
        # Define regular expressions for detecting prompts and answers
        prompt_pattern = re.compile(r'Prompt \d+:')
        answer_pattern = re.compile(r'Answer \d+:')
        
        # Use the patterns to find all prompts and answers start positions
        prompt_positions = [match.start() for match in prompt_pattern.finditer(s)]
        answer_positions = [match.start() for match in answer_pattern.finditer(s)]
        
        # Extract each prompt + answer combined and store in the list
        combined_prompts_and_answers = [s[prompt_positions[i]:prompt_positions[i+1] if i+1 < len(prompt_positions) else None].strip() for i in range(len(prompt_positions))]
        
        return combined_prompts_and_answers

    def request_new_example(self) -> str:
        topic = random.choice(self.topics)
        prompt = f"Create a new example about {topic}."
        print(prompt)
        messages = [
            {
                "role": "system",
                "content": "I want to train a chatbot to perform tasks and create code in Python, in particular, I want to be able to ask the chatbot to help me solve whatever problem that requires code creation.\nFrom now, each time I give you any input, create a conversation of at least 5 interactions between the chatbot and a user. The interactions should be about the same topic that changes or enhances the same piece of code. Make sure to ask the bot to create code changes in each interaction. The asks by the user should be challenging. The bot should only give the complete code that is ready to be used. No explanations nor summaries."
            },
            {
                "role": "user",
                "content": "Create a new example about a digital library."
            },
            {
                "role": "assistant",
                "content": "Prompt 1:\nI need a Python program to manage a digital library. The program should allow me to add books with title and author, retrieve a book by its title, and list all books available.\n\nAnswer 1:\n```python\nclass Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n\nclass Library:\n    def __init__(self):\n        self.books = []\n\n    def add_book(self, title, author):\n        book = Book(title, author)\n        self.books.append(book)\n\n    def retrieve_book(self, title):\n        for book in self.books:\n            if book.title == title:\n                return book\n\n    def list_books(self):\n        return [(book.title, book.author) for book in self.books]\n```\n\nPrompt 2:\nI want to add a feature to remove a book from the library by its title.\n\nAnswer 2:\n```python\nclass Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n\nclass Library:\n    def __init__(self):\n        self.books = []\n\n    def add_book(self, title, author):\n        book = Book(title, author)\n        self.books.append(book)\n\n    def remove_book(self, title):\n        self.books = [book for book in self.books if book.title != title]\n\n    def retrieve_book(self, title):\n        for book in self.books:\n            if book.title == title:\n                return book\n\n    def list_books(self):\n        return [(book.title, book.author) for book in self.books]\n```\n\nPrompt 3:\nI want the library to keep track of how many times each book has been retrieved.\n\nAnswer 3:\n```python\nclass Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n        self.retrieve_count = 0\n\nclass Library:\n    def __init__(self):\n        self.books = []\n\n    def add_book(self, title, author):\n        book = Book(title, author)\n        self.books.append(book)\n\n    def remove_book(self, title):\n        self.books = [book for book in self.books if book.title != title]\n\n    def retrieve_book(self, title):\n        for book in self.books:\n            if book.title == title:\n                book.retrieve_count += 1\n                return book\n\n    def list_books(self):\n        return [(book.title, book.author, book.retrieve_count) for book in self.books]\n```\n\nPrompt 4:\nI want a feature to list the top 5 most retrieved books in the library.\n\nAnswer 4:\n```python\nclass Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n        self.retrieve_count = 0\n\nclass Library:\n    def __init__(self):\n        self.books = []\n\n    def add_book(self, title, author):\n        book = Book(title, author)\n        self.books.append(book)\n\n    def remove_book(self, title):\n        self.books = [book for book in self.books if book.title != title]\n\n    def retrieve_book(self, title):\n        for book in self.books:\n            if book.title == title:\n                book.retrieve_count += 1\n                return book\n\n    def list_books(self):\n        return [(book.title, book.author, book.retrieve_count) for book in self.books]\n\n    def top_retrieved_books(self, n=5):\n        sorted_books = sorted(self.books, key=lambda book: book.retrieve_count, reverse=True)\n        return [(book.title, book.author, book.retrieve_count) for book in sorted_books[:n]]\n```\n\nPrompt 5:\nI want to add a publication year for each book and a method to retrieve books published in a certain year.\n\nAnswer 5:\n```python\nclass Book:\n    def __init__(self, title, author, year):\n        self.title = title\n        self.author = author\n        self.year = year\n        self.retrieve_count = 0\n\nclass Library:\n    def __init__(self):\n        self.books = []\n\n    def add_book(self, title, author, year):\n        book = Book(title, author, year)\n        self.books.append(book)\n\n    def remove_book(self, title):\n        self.books = [book for book in self.books if book.title != title]\n\n    def retrieve_book(self, title):\n        for book in self.books:\n            if book.title == title:\n                book.retrieve_count += 1\n                return book\n\n    def retrieve_books_by_year(self, year):\n        return [book for book in self.books if book.year == year]\n\n    def list_books(self):\n        return [(book.title, book.author, book.year, book.retrieve_count) for book in self.books]\n\n    def top_retrieved_books(self, n=5):\n        sorted_books = sorted(self.books, key=lambda book: book.retrieve_count, reverse=True)\n        return [(book.title, book.author, book.year, book.retrieve_count) for book in sorted_books[:n]]\n```"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        return self.generate_chat_completion(messages, 0.25)
