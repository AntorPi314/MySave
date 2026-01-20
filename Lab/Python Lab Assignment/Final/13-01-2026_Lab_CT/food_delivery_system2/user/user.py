from abc import ABC, abstractmethod

class User(ABC):
    platform_name = "My Food Delivery System"

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def calculate_discount(self, total):
        pass

    @classmethod
    def get_platform_name(cls):
        return cls.platform_name
    
    