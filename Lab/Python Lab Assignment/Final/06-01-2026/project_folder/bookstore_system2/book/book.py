
class Book:
    def __init__(self, title, author, isbn, price, stock):

        self.title = title
        self.author = author
        self.isbn = isbn
        self.__price = price
        self.__stock = stock


    @property
    def price(self):
        return self.__price
    
    @staticmethod
    def validate_isbn(isbn):
        return len(str(isbn)) > 6
    
    @property
    def stock(self):
        return self.__stock

    



