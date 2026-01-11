class Book:
    def __init__(self, title, author, isbn, price, stock):
        self.title = title
        self.author = author
        
        # Validate ISBN using static method
        if not Book.validate_isbn(isbn):
            raise ValueError("ISBN must be more than 6 characters.")
        self.isbn = isbn
        
        self.__price = price  # Private
        self.__stock = stock  # Private

    @property
    def price(self):
        # Read-only access to private price
        return self.__price

    # No setter for price makes it read-only

    @staticmethod
    def validate_isbn(isbn):
        return len(isbn) > 6
        
    def __str__(self):
        return f"{self.title} by {self.author}"