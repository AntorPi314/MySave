
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
            raise ValueError("Value must be greater or equal to zero")
        self.__service_charge = value

    @staticmethod
    def validate_restaurant_id(rid):
        return len(str(rid)) > 5
    

    