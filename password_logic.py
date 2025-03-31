import random
import string
from tkinter import messagebox
from data_manager import DataManager
from encryption import Encryptor

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
            
