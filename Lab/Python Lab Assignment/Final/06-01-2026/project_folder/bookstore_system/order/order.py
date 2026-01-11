from bookstore_system.utils.utils import calculate_price

class Order:
    def __init__(self, user):
        self.user = user
        self.order_items = {}  # dictionary -> book : quantity

    def add_item(self, book, quantity):
        if book in self.order_items:
            self.order_items[book] += quantity
        else:
            self.order_items[book] = quantity
        print(f"Added {quantity} x '{book.title}' to cart.")

    def remove_items(self, book):
        if book in self.order_items:
            del self.order_items[book]
            print(f"Removed '{book.title}' from cart.")
        else:
            print("Item not found in order.")

    def total_price(self):
        raw_total = 0.0
        
        # Calculate raw total using utils function
        for book, quantity in self.order_items.items():
            # Accessing read-only property 'price'
            item_total = calculate_price(book.price, quantity)
            raw_total += item_total

        # Apply user discount
        discount = self.user.calculate_discount(raw_total)
        final_price = raw_total - discount
        
        return final_price