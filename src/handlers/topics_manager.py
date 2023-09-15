import os
import json
import random

class TopicsDataManager:
    def __init__(self):
        self.sql_data = self._load_sql_data()

    def _load_sql_data(self):
        """Load the SQL data from the json file."""
        script_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(script_dir, 'sql_choices.json')
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    def _get_random_least_used(self, category):
        """Get one of the least used items from a category randomly."""
        sorted_items = sorted(self.sql_data[category], key=lambda x: x['count'])
        least_used_count = sorted_items[0]['count']
        
        # Filter the items that have the least used count
        least_used_items = [item['name'] for item in sorted_items if item['count'] == least_used_count]
        
        # Return a random item from the least used items
        return random.choice(least_used_items)

    def _increment_count(self, category, item_name):
        """Increment the count of the given item name in the given category."""
        for item in self.sql_data[category]:
            if item['name'] == item_name:
                item['count'] += 1
                break

    def _save_data(self):
        """Save the modified data back to the json file."""
        script_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(script_dir, 'sql_choices.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(self.sql_data, json_file, indent=4)

    def random_sql(self, category):
        """Get a random item from a category and increment its count."""
        item_name = self._get_random_least_used(category)
        self._increment_count(category, item_name)
        self._save_data()
        return item_name    
