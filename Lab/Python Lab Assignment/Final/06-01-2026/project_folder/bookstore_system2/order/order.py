from utils.utils import calculate_price

class Order:

    def __init__(self, user):
        self.user = user
        self.order_items = {} # (dictionary -> book : quantity)

    def add_item(self, book):
        if book in self.order_items:
            if book.stock < self.order_items[book]:
                self.order_items[book] += 1
            else:
                raise Exception("Stock Out")
        else:
            self.order_items[book] = 1

        pass
    
    def remove_items(self, book):
        if book in self.order_items:
            del self.order_items[book]
    
    def total_price(self):
        total = 0
        for k, v in self.order_items.items():
            total += k.price * v
        
        return calculate_price(total, self.user.calculate_discount(total))

     



