"""
password_generator.py – Generates a secure random password and inserts it into a Tkinter entry field.

Uses uppercase, lowercase, digits, and special characters.
"""

import random
import string

def generate_password(entry_widget):
    """
    Generates a 12-character secure password using letters, digits, and symbols.
    Inserts the result into the provided Tkinter entry widget.
    """
    # Define character pool for secure password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate random password
    password = ''.join(random.choices(characters, k=12))

    # Replace any existing text in the entry field with the new password
    entry_widget.delete(0, 'end')
    entry_widget.insert(0, password)
