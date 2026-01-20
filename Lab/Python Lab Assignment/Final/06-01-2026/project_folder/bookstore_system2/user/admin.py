from .user import User

class Admin(User):
    
    def __init__(self, username, password):
        super().__init__(username, password)


    def get_role(self):
        return "Admin"
    

    def calculate_discount(self, total):
        return total*0.20
