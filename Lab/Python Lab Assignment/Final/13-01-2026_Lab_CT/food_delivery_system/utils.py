class myError(Exception):
    pass

def calculate_price(amount, tax=0):
    return amount - tax
