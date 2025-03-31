import random
import string
from tkinter import messagebox
from data_manager import DataManager
from encryption import Encryptor
import json
from tkinter import simpledialog, messagebox
from werkzeug.security import check_password_hash, generate_password_hash

CONFIG_FILE = "config.json"

class PasswordLogic:
    def __init__(self):
        self.data_manager = DataManager()
        self.encryptor = Encryptor()

    def generate_password(self, length=12) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(characters, k=length))
        return password

    def save_password(self, website, email, password):
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
        entry = self.data_manager.load(website)
        if not entry:
            return None

        try:
            email = self.encryptor.decrypt(entry["email"])
            password = self.encryptor.decrypt(entry["password"])
            return email, password
        except Exception:
            return None
    def reset_master_password(self):
        # Step 1: Ask for current password
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

        # Step 2: Verify old password
        if not check_password_hash(stored_hash, current_pw):
            messagebox.showerror("Access Denied", "Incorrect master password.")
            return

        # Step 3: Ask for new password
        new_pw = simpledialog.askstring("New Password", "Enter new master password:", show="*")
        confirm_pw = simpledialog.askstring("Confirm Password", "Re-enter new master password:", show="*")

        if not new_pw or not confirm_pw:
            return

        if new_pw != confirm_pw:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        # Step 4: Update config.json
        new_hash = generate_password_hash(new_pw)
        config["master_password"] = new_hash

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Success", "Master password has been reset.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save new password: {e}")

    def delete_password(self, website):
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

            
