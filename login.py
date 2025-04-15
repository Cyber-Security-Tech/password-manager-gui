"""
login.py – Launches the master password login screen for the Password Manager.

This is the entry gate to the full application and verifies access via
a hashed master password stored in config.json.
"""

import tkinter as tk
from tkinter import messagebox
import json
from werkzeug.security import check_password_hash

CONFIG_FILE = "config.json"

class LoginWindow(tk.Tk):
    """
    Master password login window. On success, the main app is launched.
    """

    def __init__(self, on_success):
        """
        Initializes the login UI and binds enter key for quick login.
        """
        super().__init__()
        self.title("Login")
        self.config(padx=50, pady=50)
        self.on_success = on_success

        tk.Label(text="Enter Master Password:").grid(row=0, column=0)
        self.password_entry = tk.Entry(width=30, show="*")
        self.password_entry.grid(row=1, column=0)
        self.password_entry.focus()

        tk.Button(text="Login", width=30, command=self.check_password).grid(row=2, column=0, pady=10)

        # Bind "Enter" key to trigger login
        self.bind('<Return>', lambda event: self.check_password())

    def check_password(self):
        """
        Validates entered master password against the hashed value in config.json.
        Launches the main app if correct, shows error otherwise.
        """
        entered_password = self.password_entry.get()

        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "config.json not found.")
            return

        stored_hash = config.get("master_password")
        if check_password_hash(stored_hash, entered_password):
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("Access Denied", "Incorrect master password.")
