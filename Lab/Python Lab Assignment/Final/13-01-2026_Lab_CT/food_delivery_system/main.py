# Develop an Online Food Delivery Management System using a reusable Python module named food_delivery_system.
#  The system must be modular and include proper exception handling.

# The module must contain four sub-modules: user, restaurant, order, and utils.

# Inside the user module, create an abstract class User with a class variable platform_name 
# and instance attributes user_id and name. Initialize all attributes using a constructor. 
# Define two abstract methods get_role() and calculate_discount(total). 
# Add a class method get_platform_name(). Create a child class Customer that 
# inherits from User and implements all abstract methods.

# Also inside the user module, create another class Delivery Partner with attributes partner_id and vehicle_type.

# Create a class PremiumCustomer that demonstrates multiple inheritance by inheriting from both Customer 
# and Delivery Partner, and includes an additional attribute membership_level.

# Inside the restaurant module, create a parent class Restaurant with attributes restaurant_id, 
# name, and service_charge (private). Use property decorators to define charge (getter and setter) with valid con.
# Add a static method validate_restaurant_id(rid) to check whether the ID length is greater than 5 characters.

# Create a child class CloudKitchen that inherits from Restaurant, and another child class ExpressCloudKitchen 
# that inherits from CloudKitchen to demonstrate multilevel inheritance. Add a method get_delivery_time() and 
# override it in child classes to support polymorphism.

# Inside the order module, create a class Order with attributes user, restaurant, and order_items 
# (dictionary item: quantity). Add methods add_item(*items), **remove_item(kwargs), get_item_list() 
# using comprehension, and total_price(). The total_price() method must use user-specific discount logic. 

# solve this in python




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

    





