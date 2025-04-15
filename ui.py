"""
ui.py – Tkinter GUI for the Password Manager app.

Includes:
- Login screen with master password
- Entry and display fields for website/email/password
- Password generation and clipboard copy
- Dropdown for multiple saved accounts per website
- Full CRUD functionality: save, search, delete, reset master password
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from password_logic import PasswordLogic
from login import LoginWindow

class PasswordManagerUI(tk.Tk):
    """
    Main GUI application window for the password manager.
    """

    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.config(padx=50, pady=30)

        # App state
        self.logic = PasswordLogic()
        self.account_selector = None
        self.selected_account = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self):
        """
        Builds all labels, entries, and buttons in the main window.
        """
        self.canvas = tk.Canvas(width=100, height=100, highlightthickness=0)
        self.canvas.grid(row=0, column=1, pady=(0, 20))

        # Labels
        ttk.Label(text="Website:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(text="Email/Username:").grid(row=2, column=0, sticky="e", pady=5)
        ttk.Label(text="Password:").grid(row=3, column=0, sticky="e", pady=5)

        # Entry fields
        self.website_entry = ttk.Entry(width=35)
        self.website_entry.grid(row=1, column=1, columnspan=2, pady=5)
        self.website_entry.focus()

        self.email_entry = ttk.Entry(width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2, pady=5)

        self.password_entry = ttk.Entry(width=35, show="*")
        self.password_entry.grid(row=3, column=1, columnspan=2, pady=5)

        # Show/Hide checkbox
        ttk.Checkbutton(
            text="Show Password",
            variable=self.show_password,
            command=self._toggle_password_visibility
        ).grid(row=4, column=1, sticky="w", padx=5, pady=(0, 5))

        # Generate button
        ttk.Button(
            text="Generate",
            width=10,
            command=self._generate_password
        ).grid(row=4, column=2, sticky="e", padx=5)

        # Main action buttons
        ttk.Button(text="Add", width=36, command=self._add_password).grid(row=5, column=1, columnspan=2, pady=5)
        ttk.Button(text="Search", width=36, command=self._search_password).grid(row=6, column=1, columnspan=2, pady=5)
        ttk.Button(text="Reset Master Password", width=36, command=self._reset_master_password).grid(row=7, column=1, columnspan=2, pady=5)
        ttk.Button(text="Delete Entry", width=36, command=self._delete_password).grid(row=8, column=1, columnspan=2, pady=5)

    def _search_password(self):
        """
        Looks up saved credentials for the website.
        If multiple entries exist, shows a dropdown for selection.
        """
        website = self.website_entry.get().strip()
        if not website:
            messagebox.showwarning(title="Oops", message="Enter a website to search.")
            return

        results = self.logic.search_password(website)
        if not results:
            messagebox.showerror(title="Not Found", message="No entry found for that website.")
            return

        if len(results) == 1:
            email, password = results[0]
            self._fill_credentials(email, password)
        else:
            # Multiple entries – allow user to select from dropdown
            account_map = {
                f"{i+1}. {email}": (email, password)
                for i, (email, password) in enumerate(results)
            }
            self.selected_account.set(next(iter(account_map)))

            if self.account_selector:
                self.account_selector.destroy()

            self.account_selector = tk.OptionMenu(
                self,
                self.selected_account,
                *account_map.keys(),
                command=lambda selected: self._fill_credentials(*account_map[selected])
            )
            self.account_selector.grid(row=9, column=1, columnspan=2, sticky="ew", pady=5)
            messagebox.showinfo("Multiple Accounts", "Select an account from the dropdown.")

    def _fill_credentials(self, email, password):
        """
        Autofills the email and password fields with the selected entry.
        """
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def _toggle_password_visibility(self):
        """
        Toggles between showing and hiding the password field.
        """
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def _delete_password(self):
        """
        Deletes the password entry for the current website.
        """
        website = self.website_entry.get().strip()
        self.logic.delete_password(website)
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def _reset_master_password(self):
        """
        Resets the master password through the logic layer.
        """
        self.logic.reset_master_password()

    def _generate_password(self):
        """
        Generates a password, autofills the field, and copies to clipboard.
        """
        password = self.logic.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Copy to clipboard and alert user
        self.clipboard_clear()
        self.clipboard_append(password)
        self.focus_force()
        self.update_idletasks()
        self.update()

        messagebox.showinfo("Copied!", "Password copied to clipboard.")

    def _add_password(self):
        """
        Saves a new password entry to storage.
        """
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        self.logic.save_password(website, email, password)

        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

def start_app():
    """
    Launches the password manager UI after login validation.
    """
    app = PasswordManagerUI()
    app.mainloop()

if __name__ == "__main__":
    login = LoginWindow(on_success=start_app)
    login.mainloop()
