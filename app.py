# app.py
from login import LoginWindow
from ui import start_app

if __name__ == "__main__":
    login = LoginWindow(on_success=start_app)
    login.mainloop()
