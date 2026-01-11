from abc import ABC, abstractmethod

class User(ABC):
    shop_name = "Python BookStore"  # Class variable
    _existing_usernames = set()     # To track unique usernames

    def __init__(self, username, password):
        # Username uniqueness check
        if username in User._existing_usernames:
            raise ValueError(f"Username '{username}' already exists.")
        
        # Password length validation
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long.")

        self.username = username
        self.__password = password  # Private attribute
        
        # Add to existing usernames
        User._existing_usernames.add(username)

    @classmethod
    def get_shop_name(cls):
        return cls.shop_name

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def calculate_discount(self, total):
        pass