from tkinter import *
from password_generator import generate_password
from save import save_password

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=0, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=1, column=0)

password_label = Label(text="Password:")
password_label.grid(row=2, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=0, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=1, column=1, columnspan=2)
email_entry.insert(0, "example@email.com")

password_entry = Entry(width=21)
password_entry.grid(row=2, column=1)

# Buttons
generate_button = Button(text="Generate", command=lambda: generate_password(password_entry))
generate_button.grid(row=2, column=2)

add_button = Button(text="Add", width=36, command=lambda: save_password(website_entry, email_entry, password_entry))
add_button.grid(row=3, column=1, columnspan=2)

window.mainloop()
