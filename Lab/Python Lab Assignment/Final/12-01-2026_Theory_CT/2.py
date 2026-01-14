class Vehicle:
    def __init__(self, model, registration_number, price_per_day):
        self.model = model
        self.registration_number = registration_number
        self.price_per_day = price_per_day
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)

class PremiumService:
    def __init__(self, service_name, service_cost):
        self.service_name = service_name
        self.service_cost = service_cost

class RentalDetails:
    def __init__(self, base_price, registration_number):
        self.__base_price = base_price  # Private attribute
        self._registration_number = registration_number  # Protected attribute

    # Getter for base_price
    @property
    def base_price(self):
        return self.__base_price

    # Setter for base_price
    @base_price.setter
    def base_price(self, value):
        self.__base_price = value

    # Getter for registration_number (Read-only)
    @property
    def reg_number(self):
        return self._registration_number

class PremiumVehicle(Vehicle, RentalDetails):
    def __init__(self, model, registration_number, price_per_day, base_price):
        # Initializing both parent classes
        Vehicle.__init__(self, model, registration_number, price_per_day)
        RentalDetails.__init__(self, base_price, registration_number)
        self.premium_services = []

    def add_service(self, service):
        self.premium_services.append(service)

    def calculate_total(self, days):
        # Total = (Price per day * days) + Base Price + All Service Costs
        service_total = sum([ps.service_cost for ps in self.premium_services])
        return (self.price_per_day * days) + self.base_price + service_total

    def display_info(self, days):
        total = self.calculate_total(days)
        print(f"--- Rental Invoice ({days} Days) ---")
        print(f"Model: {self.model}")
        print(f"Registration: {self.reg_number}") # Using protected attribute via getter
        print("Services Added:")
        if not self.premium_services:
            print("- None")
        for s in self.premium_services:
            print(f"- {s.service_name}: ${s.service_cost}")
        print(f"Total Rental Cost: ${total}")
        print("-" * 30)

# --- Demonstration ---

# 1. First Premium Vehicle: SUV with GPS
v1 = PremiumVehicle("Toyota Harrier", "DHK-1234", 50, 100)
gps = PremiumService("GPS Navigation", 15)
v1.add_service(gps)
v1.display_info(3) # 3 days rental

# 2. Second Premium Vehicle: Sedan with Child Seat and WiFi
v2 = PremiumVehicle("Honda Civic", "DHK-5678", 40, 80)
seat = PremiumService("Child Seat", 10)
wifi = PremiumService("In-car WiFi", 20)
v2.add_service(seat)
v2.add_service(wifi)
v2.display_info(5) # 5 days rental

# 3. Third Premium Vehicle: Luxury Car with Chauffeur service
v3 = PremiumVehicle("BMW 5 Series", "DHK-9999", 120, 200)
chauffeur = PremiumService("Professional Chauffeur", 50)
v3.add_service(chauffeur)
v3.display_info(2) # 2 days rental