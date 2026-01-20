from restaurant.restaurant import Restaurant

class CloudKitchen(Restaurant):

    def __init__(self, restaurant_id, name, service_charge):
        super().__init__(restaurant_id, name, service_charge)


    def get_delivery_time(self):
        return "12 Hours"