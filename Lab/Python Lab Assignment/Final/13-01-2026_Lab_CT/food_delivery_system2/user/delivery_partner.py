
class DeliveryPartner:

    def __init__(self, partner_id, vehicle_type):
        self.partner_id =partner_id
        self.vehicle_type = vehicle_type

    def get_role(self):
        return "Delivery Partner"

    def calculate_discount(self, total):
        return total * 0.20