import json
import os

class ElementRemover:
    def __init__(self, folder_path, methods_to_use):
        self.folder_path = folder_path
        self.methods_to_use = methods_to_use
        self.json_file_path = self.find_json_file()

    def find_json_file(self):
        # Search for the first JSON file in the folder
        for file in os.listdir(self.folder_path):
            if file.endswith('.json'):
                return os.path.join(self.folder_path, file)
        return None

    def process_json(self):
        if not self.json_file_path:
            print("No JSON file found in the provided folder.")
            return

        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)

            if isinstance(data, list):
                for item in data:
                    for method in self.methods_to_use:
                        if method in item:
                            print(f"Removing {method} from item")  # Debug print
                            item.pop(method, None)
            else:
                print("JSON data is not a list.")

            with open(self.json_file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print("JSON file updated successfully.")  # Confirmation print
        except Exception as e:
            print(f"An error occurred: {e}")