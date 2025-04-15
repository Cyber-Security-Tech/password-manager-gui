"""
password_logic.py – Business logic layer for the Password Manager.

Handles:
- Password generation
- Input validation
- AES encryption/decryption of stored credentials
- Master password verification and reset using hashed passwords
- Interface to DataManager for saving/loading entries
"""

import random
import string
import json
from tkinter import messagebox, simpledialog
from werkzeug.security import check_password_hash, generate_password_hash

from data_manager import DataManager
from encryption import Encryptor

CONFIG_FILE = "config.json"

class PasswordLogic:
    """
    Encapsulates all password manager operations, including encryption,
    password generation, storage, retrieval, and master password reset.
    """

    def __init__(self):
        self.data_manager = DataManager()
        self.encryptor = Encryptor()

    def generate_password(self, length=12) -> str:
        """
        Generates a secure random password with letters, digits, and symbols.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(characters, k=length))
        return password

    def save_password(self, website, email, password):
        """
        Validates inputs, encrypts credentials, and saves them via DataManager.
        """
        if not website or not email or not password:
            messagebox.showwarning(title="Oops", message="Please don’t leave any fields empty!")
            return

        is_ok = messagebox.askokcancel(
            title=website,
            message=f"Save entry?\n\nEmail: {email}\nPassword: {password}"
        )

        if is_ok:
            encrypted_email = self.encryptor.encrypt(email)
            encrypted_password = self.encryptor.encrypt(password)
            self.data_manager.save(website, encrypted_email, encrypted_password)

    def search_password(self, website):
        """
        Loads and decrypts saved credentials for a given website.
        Returns a list of (email, password) tuples or None if not found.
        """
        entries = self.data_manager.load(website)
        if not entries:
            return None

        results = []
        try:
            if isinstance(entries, dict):
                entries = [entries]

            for entry in entries:
                email = self.encryptor.decrypt(entry["email"])
                password = self.encryptor.decrypt(entry["password"])
                results.append((email, password))
        except Exception:
            return None

        return results

    def reset_master_password(self):
        """
        Securely resets the master password by verifying the old one
        and storing a hashed version of the new one.
        """
        current_pw = simpledialog.askstring("Reset Password", "Enter current master password:", show="*")
        if not current_pw:
            return

        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            stored_hash = config.get("master_password")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Could not read config file.")
            return

        # Verify old master password
        if not check_password_hash(stored_hash, current_pw):
            messagebox.showerror("Access Denied", "Incorrect master password.")
            return

        # Get and confirm new master password
        new_pw = simpledialog.askstring("New Password", "Enter new master password:", show="*")
        confirm_pw = simpledialog.askstring("Confirm Password", "Re-enter new master password:", show="*")

        if not new_pw or not confirm_pw:
            return

        if new_pw != confirm_pw:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        # Hash and store the new master password
        new_hash = generate_password_hash(new_pw)
        config["master_password"] = new_hash

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Success", "Master password has been reset.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save new password: {e}")

    def delete_password(self, website):
        """
        Confirms and deletes saved credentials for a given website.
        """
        if not website:
            messagebox.showwarning("Oops", "Enter a website to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the entry for '{website}'?")
        if not confirm:
            return

        success = self.data_manager.delete(website)
        if success:
            messagebox.showinfo("Deleted", f"Entry for '{website}' deleted.")
        else:
            messagebox.showerror("Not Found", f"No entry found for '{website}'.")
