from .user import User

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        
    def get_role(self):
        return "Admin"

    def calculate_discount(self, total):
        # Example logic: Admins get 10% discount
        return total * 0.10