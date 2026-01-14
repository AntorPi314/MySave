from user import User, Customer, DeliveryPartner, PremiumCustomer
from restaurant import Restaurant, CloudKitchen, ExpressCloundKitchen
from order import Order

u1 = Customer(101, "Antor")
pc1 = PremiumCustomer(201, "Adnan", 888, "Bike", "Golden")

ck1 = CloudKitchen(5001, "Dream Hut", 100)

o1 = Order(u1, ck1)

o1.add_item(
    ("Pizza", 600, 2),
    ("Burger", 500, 1)
)
o1.remove_item(name="Burger", price=500, qty=1)

print(o1.total_price())

    





