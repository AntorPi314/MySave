from abc import ABC, abstractmethod

class User:
    platform_name = "My Platform"

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self):
        return "User"

    @abstractmethod
    def calculate_discount(self, total):
        pass

    @classmethod
    def get_platform_name(cls):
        return cls.platform_name
    

class Customer(User):

    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def get_role(self):
        return "Customer"
    
    def calculate_discount(self, total):
        return total * .05
    

class DeliveryPartner:
    def __init__(self, partner_id, vehicle_type):
        self.partner_id = partner_id
        self.vehicle_type =vehicle_type


class PremiumCustomer(Customer, DeliveryPartner):
    def __init__(self, user_id, name, partner_id, vehicle_type, membership_level):
        super().__init__(user_id, name)
        DeliveryPartner.__init__(self, partner_id, vehicle_type)
        self.membership_level = membership_level

    def get_role(self):
        return "PremiumCustomer"
    
    def calculate_discount(self, total):
        return total * .20




