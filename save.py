from tkinter import messagebox

def save_password(website_entry, email_entry, password_entry):
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not email or not password:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty.")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"Save entry?\n\nEmail: {email}\nPassword: {password}")
    if is_ok:
        with open("data.txt", "a") as file:
            file.write(f"{website} | {email} | {password}\n")

        website_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
