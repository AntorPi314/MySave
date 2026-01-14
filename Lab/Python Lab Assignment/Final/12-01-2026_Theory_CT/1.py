

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

class Member:
    total_borrowed_books = 0

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            Member.total_borrowed_books += 1
        else: raise Exception("Error: Book already exist in borrow list")
            
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            Member.total_borrowed_books -= 1
            return book
        else: raise Exception("This book is not exist in your borrow list")


