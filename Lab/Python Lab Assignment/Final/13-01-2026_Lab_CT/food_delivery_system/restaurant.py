
class Restaurant:
    def __init__(self, restaurant_id, name, service_charge):
        self.restaurant_id = restaurant_id
        self.name = name
        self.__service_charge = service_charge

    @property
    def service_charge(self):
        return self.__service_charge
    
    @service_charge.setter
    def service_charge(self, value):
        if value < 0:
            raise Exception("Value must be greater than 0")
        else: self.__service_charge = value

    @staticmethod
    def validate_restaurant_id(rid):
        return len(rid) > 5
    

class CloudKitchen(Restaurant):
    def __init__(self, restaurant_id, name, service_charge):
        super().__init__(restaurant_id, name, service_charge)

    def get_delivery_time():
        return "7 Days"
    
class ExpressCloundKitchen(CloudKitchen):
    def __init__(self, restaurant_id, name, service_charge):
        super().__init__(restaurant_id, name, service_charge)

    def get_delivery_time():
        return "1 Day"
    

