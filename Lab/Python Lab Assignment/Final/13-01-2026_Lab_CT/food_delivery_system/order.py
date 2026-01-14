
class Order:
    def __init__(self, user, restaurant):
        self.user = user
        self. restaurant = restaurant
        self.order_items = {} # item: quantity

    def add_item(self, *items):
        for name, price, qty in items:
            try:
                if name in self.order_items:
                    self.order_items[name]['qty'] += qty
                else:
                    self.order_items[name] = {'price': price, 'qty': qty}
            except Exception as e:
                print(f"Something went wrong! >> {e}")

    def remove_item(self, **kwargs):
        name = kwargs.get("name")
        if name in self.order_items:
            self.order_items.pop(name, None)

    def get_item_list(self):
        return [v for v in self.order_items.values()]
    
    def total_price(self):
        total = sum([v['price']*v['qty'] for v in self.order_items.values()])
        total += self.restaurant.service_charge
        return total - self.user.calculate_discount(total)










