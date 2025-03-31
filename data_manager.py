import json
import os

DATA_FILE = "data/passwords.json"

class DataManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    def save(self, website, email, password):
        new_entry = {
            "email": email,
            "password": password
        }

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

    # If website already exists, convert to list or append
        if website in data:
        # Convert existing single entry to a list if needed
            if isinstance(data[website], dict):
                data[website] = [data[website]]
            data[website].append(new_entry)
        else:
            data[website] = [new_entry]

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)


    def load(self, website):
        try:
             with open(DATA_FILE, "r") as f:
                data = json.load(f)
             return data.get(website)
        except (FileNotFoundError, json.JSONDecodeError):
                return None

    def delete(self, website):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False  # File or JSON broken

        if website not in data:
            return False  # Nothing to delete

        del data[website]

        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False


