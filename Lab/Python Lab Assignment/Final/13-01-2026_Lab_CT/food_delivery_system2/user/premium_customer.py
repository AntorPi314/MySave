from user.customer import Customer
from user.delivery_partner import DeliveryPartner

class PremiumCustomer(Customer, DeliveryPartner):

    def __init__(self, user_id, name, partner_id, vehicle_type, membership_level):
        super().__init__(user_id, name)
        DeliveryPartner.__init__(self, partner_id, vehicle_type)
        self.membership_level = membership_level


    def get_role(self):
        return "Premium Customer"

    def calculate_discount(self, total):
        return total * 0.25 