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
            website: {
                "email": email,
                "password": password
            }
        }

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

        data.update(new_entry)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Saved {website} to file.")
