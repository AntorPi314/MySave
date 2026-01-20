from user.user import User 

class Customer(User):

    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def get_role(self):
        return "Customer"

    def calculate_discount(self, total):
        return total * 0.15
    
