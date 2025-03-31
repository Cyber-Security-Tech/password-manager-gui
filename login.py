import tkinter as tk
from tkinter import messagebox
import json
from werkzeug.security import check_password_hash

CONFIG_FILE = "config.json"

class LoginWindow(tk.Tk):
    def __init__(self, on_success):
        super().__init__()
        self.title("Login")
        self.config(padx=50, pady=50)
        self.on_success = on_success

        tk.Label(text="Enter Master Password:").grid(row=0, column=0)
        self.password_entry = tk.Entry(width=30, show="*")
        self.password_entry.grid(row=1, column=0)
        self.password_entry.focus()

        tk.Button(text="Login", width=30, command=self.check_password).grid(row=2, column=0, pady=10)

        self.bind('<Return>', lambda event: self.check_password())

    def check_password(self):
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
