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




# main.py
from bookstore_system.user.admin import Admin
from bookstore_system.user.customer import Customer
from bookstore_system.book.book import Book
from bookstore_system.order.order import Order
from bookstore_system.user.user import User

def main():
    print(f"Welcome to {User.get_shop_name()} System\n")

    try:
        # 1. Create Users (Testing Exception Handling for password/duplicate)
        try:
            # Short password error check
            bad_user = Customer("test_bad", "123") 
        except ValueError as e:
            print(f"Expected Error caught: {e}")

        admin = Admin("Antor", "admin123")
        customer = Customer("Tamim", "pass1234")
        # customer2 = Customer("Adnan", "pass5678")
        
        print(f"Users Created: {admin.username} ({admin.get_role()}), {customer.username} ({customer.get_role()})")

        # 2. Create Books
        # ISBN validation check
        try:
            bad_book = Book("Bad Book", "Author", "123", 100, 5)
        except ValueError as e:
            print(f"Expected Error caught: {e}")

        book1 = Book("Python Basics", "Jane Doe", "978-12345", 500, 10)
        book2 = Book("Advanced AI", "John Smith", "978-67890", 1200, 5)
        
        # Check read-only price
        # book1.price = 600  # This would raise an AttributeError

        # 3. Process Order for Customer
        print("\n--- Processing Order ---")
        order = Order(customer)
        
        # Add items
        order.add_item(book1, 2) # 2 * 500 = 1000
        order.add_item(book2, 1) # 1 * 1200 = 1200
        
        # Total raw: 2200. Customer Discount (5%): 110. Final: 2090.
        final_bill = order.total_price()
        
        print(f"Total Bill for {customer.username}: ${final_bill}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()