from handlers.openai_handler import OpenAIApiHandler as AIHandler

class PythonCodeCreation(AIHandler):
    def __init__(self):
        super().__init__()

    def separate_prompt_and_answer(self,text):
        # Split the section into prompt and answer using '\nAnswer ' as a delimiter
        prompt, answer = text.split('\nAnswer ')
        # Clean up the prompt and answer by stripping leading/trailing whitespaces
        prompt = prompt.strip().replace('Prompt ', '').replace('Input:\nNext\nOutput:\n', '')      
        # Remove the index (like "5:") from the start of the prompt text
        prompt = ':'.join(prompt.split(':')[1:]).strip()   
        answer = ':'.join(answer.split(':')[1:]).strip()
        return prompt, answer

    def extract_prompts_and_answers(self,text:str):
        # Split the input text into separate sections
        sections = text.split("Input:\nNext\nOutput:\n")  
        # Initialize an empty list to store the extracted prompts and answers
        prompts_and_answers = []       
        # Iterate through each section and further split it into prompt and answer
        for section in sections:
            # Split the section into prompt and answer using the "\nAnswer" as a delimiter
            prompt, answer = section.split('\nAnswer ')           
            # Clean up the prompt and answer, then combine them into a single string
            prompt = prompt.strip()
            answer = "Answer " + answer.strip()
            combined = f'{prompt}\n{answer}'       
            # Append the combined string to the list of prompts and answers
            prompts_and_answers.append(combined) 
        # Return the list of strings, each containing a prompt and an associated answer
        return prompts_and_answers[0], prompts_and_answers[1], prompts_and_answers[2], prompts_and_answers[3], prompts_and_answers[4]

    def request_new_example(self) -> str:
        messages = [
            {
                "role":"system",
                "content":"I want to train a chatbot to perform tasks and create code in Python, in particular.\nFrom now, each time I give you as input \"New example\" create an initial prompt between the user and the bot.\nHere is an example:\nInput: \nNew example\nOutput:\nPrompt 1:\nI need a Python program to manage a simple ticket booking system. The program should allow me to add events with a certain number of tickets available. It should also allow users to book tickets for an event and check the number of tickets remaining for that event.\n\nAnswer 1:\n```python\nclass Event:\n    def __init__(self, name, total_tickets):\n        self.name = name\n        self.total_tickets = total_tickets\n        self.booked_tickets = 0\n\n    def book_ticket(self, num_tickets):\n        if self.booked_tickets + num_tickets <= self.total_tickets:\n            self.booked_tickets += num_tickets\n        else:\n            print(\"Not enough tickets available\")\n            \n    def remaining_tickets(self):\n        return self.total_tickets - self.booked_tickets\n\nclass BookingSystem:\n    def __init__(self):\n        self.events = {}\n\n    def add_event(self, name, total_tickets):\n        self.events[name] = Event(name, total_tickets)\n\n    def book_ticket(self, event_name, num_tickets):\n        if event_name in self.events:\n            self.events[event_name].book_ticket(num_tickets)\n        else:\n            print(\"Event not found\")\n            \n    def remaining_tickets(self, event_name):\n        if event_name in self.events:\n            return self.events[event_name].remaining_tickets()\n        else:\n            print(\"Event not found\")\n```\nIf I input \"Next\" then I want you to continue the last conversation between the user and the bot, here are the follow-up examples:\nInput:\nNext\nOutput:\nPrompt 2:\nI want to add a feature to list all the events along with their remaining tickets.\n\nAnswer 2:\n```python\nclass Event:\n    def __init__(self, name, total_tickets):\n        self.name = name\n        self.total_tickets = total_tickets\n        self.booked_tickets = 0\n\n    def book_ticket(self, num_tickets):\n        if self.booked_tickets + num_tickets <= self.total_tickets:\n            self.booked_tickets += num_tickets\n        else:\n            print(\"Not enough tickets available\")\n            \n    def remaining_tickets(self):\n        return self.total_tickets - self.booked_tickets\n\nclass BookingSystem:\n    def __init__(self):\n        self.events = {}\n\n    def add_event(self, name, total_tickets):\n        self.events[name] = Event(name, total_tickets)\n\n    def book_ticket(self, event_name, num_tickets):\n        if event_name in self.events:\n            self.events[event_name].book_ticket(num_tickets)\n        else:\n            print(\"Event not found\")\n            \n    def remaining_tickets(self, event_name):\n        if event_name in self.events:\n            return self.events[event_name].remaining_tickets()\n        else:\n            print(\"Event not found\")\n\n    def list_events(self):\n        for event_name, event in self.events.items():\n            print(event_name, event.remaining_tickets())\n```\nInput:\nNext\nOutput:\nPrompt 3:\nI want to add a feature to cancel a booking and increase the number of available tickets for an event.\n\nAnswer 3:\n```python\nclass Event:\n    def __init__(self, name, total_tickets):\n        self.name = name\n        self.total_tickets = total_tickets\n        self.booked_tickets = 0\n\n    def book_ticket(self, num_tickets):\n        if self.booked_tickets + num_tickets <= self.total_tickets:\n            self.booked_tickets += num_tickets\n        else:\n            print(\"Not enough tickets available\")\n            \n    def cancel_booking(self, num_tickets):\n        if self.booked_tickets - num_tickets >= 0:\n            self.booked_tickets -= num_tickets\n        else:\n            print(\"Cannot cancel more tickets than booked\")\n            \n    def remaining_tickets(self):\n        return self.total_tickets - self.booked_tickets\n\nclass BookingSystem:\n    def __init__(self):\n        self.events = {}\n\n    def add_event(self, name, total_tickets):\n        self.events[name] = Event(name, total_tickets)\n\n    def book_ticket(self, event_name, num_tickets):\n        if event_name in self.events:\n            self.events[event_name].book_ticket(num_tickets)\n        else:\n            print(\"Event not found\")\n            \n    def cancel_booking(self, event_name, num_tickets):\n        if event_name in self.events:\n            self.events[event_name].cancel_booking(num_tickets)\n        else:\n            print(\"Event not found\")\n            \n    def remaining_tickets(self, event_name):\n        if event_name in self.events:\n            return self.events[event_name].remaining_tickets()\n        else:\n            print(\"Event not found\")\n\n    def list_events(self):\n        for event_name, event in self.events.items():\n            print(event_name, event.remaining_tickets())\n```\nNotice how these are the complete Python programs for each prompt, with all functions included in each answer. They do not have any comments or omissions, and you can copy and paste each one as a standalone program. I want to have those. After answer 5, I'll ask for a new example."
            },
            {
                "role":"user",
                "content":"New example"
            }
        ]
        return self.generate_chat_completion(messages)
