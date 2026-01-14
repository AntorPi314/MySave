# Group 2: Online Shopping and Order Processing System

# Design a backend simulation for an online shop. Implement a base class User containing attributes
# _user_id (int), _username (str), and _password (str).
# Implement methods login() and __str__().
# This class must demonstrate constructor usage, encapsulation,
# string formatting, and conditional statements.

# Create a class Customer that inherits from User and contains _balance (float) and cart (list).
# Implement methods add_to_cart(*product_ids), checkout(discount=0), and a @property for balance.
# This class must demonstrate inheritance, property decorator, args usage,
# default arguments, loops, and exception handling.

# Create a class Admin that inherits from User and contains attribute role (str).
# Implement methods add_product(name, price, stock) and update_stock(product_id, quantity).
# Use a static method validate_price(price) and a class method create_admin(data).
# This class must demonstrate static method, class method, inheritance,
# validation, and dictionary operations.

# Create classes Product and Order where Product contains product_id, name, price, and stock,
# and Order contains order_id, items, total_price, and status.
# Implement methods calculate_total(*prices, tax=0.1) and __str__().
# The system controller class ShopSystem must manage collections and implement
# order_generator(), sort_orders(key_name), and revenue calculation using
# map, filter, reduce, generators, sorting with custom key, and exception handling.




class User:
    def __init__(self, user_id: int, username: str, password: str):
        self._user_id = user_id
        self._username = username
        self._password = password

    def login(self, username, password):
        if self._username == username and self._password == password:
            return "Login successful"
        return "Invalid credentials"

    def __str__(self):
        return f"UserID: {self._user_id}, Username: {self._username}"


# Create a class Customer that inherits from User and contains _balance (float) and cart (list).
# Implement methods add_to_cart(*product_ids), checkout(discount=0), and a @property for balance.
# This class must demonstrate inheritance, property decorator, args usage,
# default arguments, loops, and exception handling. #


class Customer(User):
    def __init__(self, user_id, username, password, balance: float):
        super().__init__(user_id, username, password)
        self._balance = balance
        self.cart = list()

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def add_to_cart(self, *product_ids):
        for p in product_ids:
            self.cart.append(p)

    def checkout(self, discount=0):
        try:
            total = sum([p.price for p in self.cart])
            total -= discount

            if total > self._balance:
                raise Exception("Insufficient balance")

            self._balance -= total
            self.cart.clear()
            return f"Checkout successful. Remaining balance: {self._balance}"

        except Exception as e:
            return str(e)


# Create a class Admin that inherits from User and contains attribute role (str).
# Implement methods add_product(name, price, stock) and update_stock(product_id, quantity).
# Use a static method validate_price(price) and a class method create_admin(data).
# This class must demonstrate static method, class method, inheritance,
# validation, and dictionary operations. #


class Admin(User):
    products = {}

    def __init__(self, user_id, username, password, role):
        super().__init__(user_id, username, password)
        self.role = role

    @staticmethod
    def validate_price(price):
        return price > 0

    def add_product(self, name, price, stock):
        if not Admin.validate_price(price):
            raise ValueError("Invalid price")

        product_id = len(Admin.products) + 1
        Admin.products[product_id] = Product(product_id, name, price, stock)
        return Admin.products[product_id]

    def update_stock(self, product_id, quantity):
        if product_id in Admin.products:
            Admin.products[product_id].stock += quantity

    @classmethod
    def create_admin(cls, data):
        return cls(
            data["user_id"],
            data["username"],
            data["password"],
            data["role"]
        )


# Create classes Product and Order where Product contains product_id, name, price, and stock,
# and Order contains order_id, items, total_price, and status.
# Implement methods calculate_total(*prices, tax=0.1) and __str__().
# The system controller class ShopSystem must manage collections and implement order_generator(),
# sort_orders(key_name), and revenue calculation using
# map, filter, reduce, generators, sorting with custom key, and exception handling. #


from functools import reduce


class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"ProductID: {self.product_id}, Name: {self.name}, Price: {self.price}, Stock: {self.stock}"


class Order:
    def __init__(self, order_id, items, status="Pending"):
        self.order_id = order_id
        self.items = items
        self.total_price = self.calculate_total(*map(lambda p: p.price, items))
        self.status = status

    def calculate_total(self, *prices, tax=0.1):
        subtotal = sum(prices)
        return subtotal + (subtotal * tax)

    def __str__(self):
        return f"OrderID: {self.order_id}, Total: {self.total_price}, Status: {self.status}"


class ShopSystem:
    def __init__(self):
        self.orders = []

    def create_order(self, items):
        order = Order(len(self.orders) + 1, items)
        self.orders.append(order)
        return order

    def order_generator(self):
        for order in self.orders:
            yield order

    def sort_orders(self, key_name):
        return sorted(self.orders, key=lambda o: getattr(o, key_name))

    def total_revenue(self):
        try:
            completed_orders = filter(lambda o: o.status == "Completed", self.orders)
            total = 0
            for o in completed_orders:
                total += o.total_price
            return total
            # return reduce(lambda total, o: total + o.total_price, completed_orders, 0)
        except Exception as e:
            return str(e)


# =========================
# Example Usage
# =========================

admin = Admin.create_admin({
    "user_id": 1,
    "username": "admin",
    "password": "1234",
    "role": "SuperAdmin"
})

p1 = admin.add_product("Laptop", 50000, 10)
p2 = admin.add_product("Mouse", 1000, 50)

customer = Customer(2, "Antor", "abcd", 60000)

print(customer.login("Antor", "abcd"))

customer.add_to_cart(p1, p2)

shop = ShopSystem()
order = shop.create_order(customer.cart)
order.status = "Completed"

print(order)
print(customer.checkout(discount=1000))

print("---- Orders ----")
for o in shop.order_generator():
    print(o)

print("---- Sorted Orders ----")
for o in shop.sort_orders("total_price"):
    print(o)

print("Total Revenue:", shop.total_revenue())









