import random
import string

def generate_password(entry_widget):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=12))
    entry_widget.delete(0, 'end')
    entry_widget.insert(0, password)
