"""
data_manager.py – Handles saving, loading, and deleting passwords in a structured JSON format.

Features:
- Supports multiple entries per website
- Creates 'data/passwords.json' if it doesn't exist
- Uses error handling to ensure resilience
"""

import json
import os

# Path to the password storage file
DATA_FILE = "data/passwords.json"

class DataManager:
    def __init__(self):
        """
        Initializes the data manager and ensures the data directory and file exist.
        """
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    def save(self, website, email, password):
        """
        Saves a new entry for a website. Supports multiple credentials per website.
        """
        new_entry = {
            "email": email,
            "password": password
        }

        # Load existing data or start fresh
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Handle duplicate websites by appending to a list
        if website in data:
            if isinstance(data[website], dict):
                data[website] = [data[website]]  # Convert to list
            data[website].append(new_entry)
        else:
            data[website] = [new_entry]

        # Write updated data back to the file
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, website):
        """
        Loads and returns all credentials for the given website.
        Returns None if not found or error occurs.
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            return data.get(website)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def delete(self, website):
        """
        Deletes all credentials associated with a given website.
        Returns True if successful, False if not found or error occurs.
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False  # File missing or broken

        if website not in data:
            return False  # Nothing to delete

        # Remove the website's entry
        del data[website]

        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False
