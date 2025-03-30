from data_manager import DataManager

class PasswordLogic:
    def __init__(self):
        self.data_manager = DataManager()

    def generate_password(self):
        print("Generate password clicked!")

    def save_password(self, website, email, password):
        self.data_manager.save(website, email, password)
