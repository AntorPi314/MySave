from utils.utils import myError

class Order:

    def __init__(self, user, restaurant):
        self.user = user
        self.restaurant = restaurant
        self.order_items = {}

    def add_item(self, *items):
        for i in items:
            if i in self.order_items:
                self.order_items[i] += 1
            else:
                self.order_items[i] = 1

        
    def remove_item(self, **kwargs):
        t = (kwargs["Name"], kwargs["Price"])
        if t in self.order_items:
            del self.order_items[t]
        else:
            raise myError("Item not found in your order list")

    
    def get_item_list(self):
        return [k for k in self.order_items.keys()]
    
    def total_price(self):
        total = 0
        for k, v in self.order_items.items():
            total += k[1] * v

        return total - self.user.calculate_discount(total)



