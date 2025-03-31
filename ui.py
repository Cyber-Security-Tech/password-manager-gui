import tkinter as tk
from tkinter import messagebox
from password_logic import PasswordLogic

class PasswordManagerUI(tk.Tk):

    def _search_password(self):
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
        # Multiple accounts found
        # Build label options for dropdown (we’ll show emails as identifiers)
            account_map = {f"{i+1}. {email}": (email, password) for i, (email, password) in enumerate(results)}

        # Update the selector options
            self.selected_account.set(next(iter(account_map)))  # set to first email

        # Destroy previous dropdown if it exists
            if self.account_selector:
                self.account_selector.destroy()

            self.account_selector = tk.OptionMenu(
                self,
                self.selected_account,
                *account_map.keys(),
                command=lambda selected: self._fill_credentials(*account_map[selected])
            )
            self.account_selector.grid(row=8, column=1, columnspan=2, sticky="ew", pady=5)
            messagebox.showinfo("Multiple Accounts", "Select an account from the dropdown.")


    def _fill_credentials(self, email, password):
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)


    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.config(padx=50, pady=50)
        self.logic = PasswordLogic()
        self.account_selector = None  # Will hold the dropdown widget
        self.selected_account = tk.StringVar()  # Tracks the selected dropdown option

        self._build_ui()

    def _build_ui(self):
        # Canvas (optional image/logo space)
        self.canvas = tk.Canvas(width=200, height=200)
        self.canvas.grid(row=0, column=1)

        # Labels
        tk.Label(text="Website:").grid(row=1, column=0)
        tk.Label(text="Email/Username:").grid(row=2, column=0)
        tk.Label(text="Password:").grid(row=3, column=0)

        # Entries
        self.website_entry = tk.Entry(width=35)
        self.website_entry.grid(row=1, column=1, columnspan=2)
        self.website_entry.focus()

        self.email_entry = tk.Entry(width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2)

        self.password_entry = tk.Entry(width=21)
        self.password_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(text="Generate", width=10, command=self._generate_password).grid(row=3, column=2)
        tk.Button(text="Add", width=36, command=self._add_password).grid(row=4, column=1, columnspan=2)
        tk.Button(text="Search", width=36, command=self._search_password).grid(row=5, column=1, columnspan=2)
        tk.Button(text="Reset Master Password", width=36, command=self._reset_master_password).grid(row=6, column=1, columnspan=2)
        tk.Button(text="Delete Entry", width=36, command=self._delete_password).grid(row=7, column=1, columnspan=2)

    def _delete_password(self):
        website = self.website_entry.get().strip()
        self.logic.delete_password(website)
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)


    def _reset_master_password(self):
        self.logic.reset_master_password()


    def _generate_password(self):
        password = self.logic.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Copy to clipboard (updated with window focus)
        self.clipboard_clear()
        self.clipboard_append(password)
        self.focus_force()     # Brings the window to front (important on Windows)
        self.update_idletasks()
        self.update()

        # Optional confirmation
        messagebox.showinfo("Copied!", "Password copied to clipboard.")


    def _add_password(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        self.logic.save_password(website, email, password)

        # Clear fields only if save was attempted
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

from login import LoginWindow

def start_app():
    app = PasswordManagerUI()
    app.mainloop()

if __name__ == "__main__":
    login = LoginWindow(on_success=start_app)
    login.mainloop()

