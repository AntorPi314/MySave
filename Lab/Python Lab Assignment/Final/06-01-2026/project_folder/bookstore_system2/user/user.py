from abc import ABC, abstractmethod

class User(ABC):

    shop_name = "My Book Shop"
    unique_users = set()
    
    def __init__(self, username, password):
        if User.isUniqueUser(username):
            self.username = username
            self.password = password
        else:
            raise Exception("This user is already exist!")

    @staticmethod
    def isUniqueUser(user):
        if user not in User.unique_users:
            User.unique_users.add(user)
            return True
        else:
            return False

    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def calculate_discount(self, total):
        pass
    
    @classmethod
    def get_shop_name(cls):
        return cls.shop_name











        