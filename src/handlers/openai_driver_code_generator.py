from handlers.openai_handler import OpenAIApiHandler


class DriverCodeGenerator(OpenAIApiHandler):
    def __init__(self):
        super().__init__()

    def format_user_prompt(self, code_block: str) -> str:
        lines = code_block.strip().split("\n")
        code_content = lines[1:-1]
        formatted_code = "\\n".join(line.replace("\n", "").replace(
            "\"", "\\\"") for line in code_content)
        return f"```{formatted_code}\\n```"

    def request_driver_and_example_usage(self, code_to_explain: str) -> str:
        formattedPrompt = self.format_user_prompt(code_to_explain)

        messages = [
            {
                "role": "system",
                "content": "You are a senior software developer who does not like code smells or bad coding practices. You will be helping a junior software engineer who is a fresh graduate and presents you with code that they do not entirely understand. For each piece of code I give you, I want you to create a driver function and example usage of the code. Then give me the expected output based on the code provided. Make sure to add at the end the expected output of the driver function\nI will give you the input in this format:\n```{coding_language}\n{code}\n```\nI expect the output in this format:\n```{coding_language}\n{code}\n#Example driver function\n{driver_function}\n```\n #Expected output: ```yaml\n{expected_output}\n```"
            },
            {
                "role": "user",
                "content": "```python\nclass Machinery:\n    def __init__(self, name, description, price):\n        self.name = name\n        self.description = description\n        self.price = price\n\nclass MachineryInventory:\n    def __init__(self):\n        self.machinery_list = []\n\n    def add_machinery(self, name, description, price):\n        machinery = Machinery(name, description, price)\n        self.machinery_list.append(machinery)\n\n    def retrieve_machinery(self, name):\n        for machinery in self.machinery_list:\n            if machinery.name == name:\n                return machinery\n\n    def list_machinery(self):\n        return [(machinery.name, machinery.description, machinery.price) for machinery in self.machinery_list]\n```"
            },
            {
                "role": "assistant",
                        "content": "```python\nclass Machinery:\n    def __init__(self, name, description, price):\n        self.name = name\n        self.description = description\n        self.price = price\n\nclass MachineryInventory:\n    def __init__(self):\n        self.machinery_list = []\n\n    def add_machinery(self, name, description, price):\n        machinery = Machinery(name, description, price)\n        self.machinery_list.append(machinery)\n\n    def retrieve_machinery(self, name):\n        for machinery in self.machinery_list:\n            if machinery.name == name:\n                return machinery\n\n    def list_machinery(self):\n        return [(machinery.name, machinery.description, machinery.price) for machinery in self.machinery_list]\n\n#Example driver function\ndef driver_function():\n    inventory = MachineryInventory()\n    \n    # Adding machinery\n    inventory.add_machinery(\"Excavator\", \"Used for digging.\", 50000)\n    inventory.add_machinery(\"Bulldozer\", \"Used for pushing large amounts of material.\", 70000)\n    \n    # Retrieving machinery\n    retrieved_machinery = inventory.retrieve_machinery(\"Excavator\")\n    \n    # Listing all machinery\n    all_machinery = inventory.list_machinery()\n\n    return retrieved_machinery.name, retrieved_machinery.description, retrieved_machinery.price, all_machinery\n\nresult = driver_function()\nprint(result)\n```\n\n```yaml\n('Excavator', 'Used for digging.', 50000, [('Excavator', 'Used for digging.', 50000), ('Bulldozer', 'Used for pushing large amounts of material.', 70000)])\n```\n"
            },
            {
                "role": "user",
                "content": formattedPrompt
            }
        ]

        return self.generate_chat_completion(messages)
