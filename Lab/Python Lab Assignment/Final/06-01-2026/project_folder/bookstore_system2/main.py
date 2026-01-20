# You have to develop a Online Book Store Management using python reusable module name bookstore_system.
# It must have four sub-packages user, book, order, and utils. System must have proper exception handing.

# Inside user sub-package, there will be one abstract class User with attributes shop_name (class variable),
#  username, and password (private). Here username should be unique and password not less than 4 characters.
# It must have two abstract method get_role(), calculate_discount(total), class method get_shop_name(),
# and . There should to two child class Admin and Customer. Create separate file for each class.

# In book sub-package, a parent class Book with atributes title, author, isbn, price (private + read_only)
# and stock (private). It should have one static method validate_isbn(isbn) to check lenght more than 6 character or not.

# Order sub-package contain a class Order with attributes user, order_items (dictionary -> book : quantity).
# Add methods add_item(), remove_items() and total_price().

# At last, Utils package have one utils file with one function call calculate_price, 
# use it inside order package to calculate total price.

# After completing the package, demostrate the system in main.py file.


# project_folder/
# │
# ├── bookstore_system/
# │   ├── user/
# │   │   ├── user.py       <-- Abstract Class
# │   │   ├── admin.py
# │   │   └── customer.py
# │   ├── book/
# │   │   └── book.py
# │   ├── order/
# │   │   └── order.py
# │   └── utils/
# │       └── utils.py
# │
# └── main.py

from book.book import Book
from order.order import Order
from user.admin import Admin
from user.user import User
from user.customer import Customer


b1 = Book("Book1", "Antor", 23423433, 230, 5)

u1 = Customer("Tamim", "pass1234")


o1 = Order(u1)

o1.add_item(b1)

print(o1.total_price())







