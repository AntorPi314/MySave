from .user import User

class Customer(User):
    
    def __init__(self, username, password):
        super().__init__(username, password)


    def get_role(self):
        return "Customer"
    

    def calculate_discount(self, total):
        return total*0.15