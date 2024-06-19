#  Add books to Library

import json


required_info = ["title", "author", "book_id"]


# class Book:

#     def __init__(self, book_id, title, author):
#         self.book_id = book_id
#         self.title = title
#         self.author = author

#     def __str__(self):
#         return self.title

#     def __repr__(self) -> str:
#         return self.title


class UserInterface:
    """Library User Interface"""

    def __init__(self):
        self.library = Library()

    def add_a_new_book(self):
        """
        Add a new book to the library
        """
        total_entries = int(input("Enter the number of entries you want to add: "))
        new_books = {}
        for _ in range(total_entries):
            book_record = {}
            for each_info in required_info:
                value = input(f"Enter {each_info} of the book: ")
                book_record[each_info] = value
            new_books[book_record["book_id"]] = book_record
        self.send_book_to_library(new_books)

    def send_book_to_library(self, books: dict):
        """
        Sends newly added book to the library
        param books: Books to send to library
        """
        self.library.add_books(books)

    def display_all_books(self):
        """
        Display all available books
        """
        all_books = []
        books = self.library.get_books()
        print(books)
        for each_book in self.library.get_books():
            print(each_book)
            title_of_the_books = books[each_book].get("title")
            all_books.append(title_of_the_books)
            # yield each_book
        print(f"Displaying all available books: {all_books}")
        return all_books

    def search_books(self):
        """
        Search a book
        """
        search_input = str(input("Search by Book Title or Author: "))
        searched_books = self.library.get_searched_books(search_input=search_input)
        print("Books found:")
        print(json.dumps(searched_books, indent=4))


class Library:
    """
    Library class
    """

    FILENAME = "all_books.txt"

    def __init__(self):
        self.categories = self.load_from_file()
        self.categories.setdefault("available_books", {})
        self.categories.setdefault("borrowed_books", {})

        self.available_books = self.categories.get("available_books")
        self.borrowed_books = self.categories.get("borrowed_books")

    def add_books(self, new_books: dict):
        """
        Add new books to the library
        new_books: New books
        """
        self.available_books.update(new_books)
        self.save_to_file()

    def get_searched_books(self, search_input):
        """Search a book from all books"""
        all_books = self.get_books()
        searched_books = []
        # print(all_books)
        for book_data in all_books.values():
            # print(book_data)
            for _, value in book_data.items():
                if search_input in value:
                    searched_books.append(book_data)
        return searched_books

    def get_books(self, available=True, borrowed=True):
        """
        Returns book data
        param available: Returns only available books
        param borrowed: Returns only borrowed books
        """
        books_view = {}
        if available:
            books_view.update(self.available_books)
        if borrowed:
            books_view.update(self.borrowed_books)
        return books_view

    def borrow_book(self, book_id: int):
        """
        Borrow an available book
        param book_id: ID of the book to borrow
        """
        if book_id in self.available_books:
            book_detail = self.available_books.pop(book_id)
            self.borrowed_books[book_id] = book_detail
            self.save_to_file()
        else:
            raise ValueError(
                "The provided book ID either doesn't exist or has already been borrowed"
            )

    def return_book(self, book_id: int):
        """
        Return a borrowed book
        param book_id: ID of the borowed book
        """
        if book_id in self.borrowed_books:
            book_detail = self.borrowed_books.pop(book_id)
            self.available_books[book_id] = book_detail
            self.save_to_file()
        else:
            raise ValueError(
                "The book you are trying to return either doesn't exist or was not borrowed."
            )

    def save_to_file(self):
        """
        Save library data to file
        """
        # Writing to file
        try:
            with open(self.FILENAME, "w", encoding="utf-8") as file1:
                # Writing data to a file
                book_data = json.dumps(self.categories, indent=4)
                file1.write(book_data)
        except (TypeError, ValueError, IOError) as e:
            print(f"Something went wrong while saving to file: {e}")
            raise

    def load_from_file(self):
        """
        Load library data from file
        """
        try:
            with open(self.FILENAME, "r", encoding="utf-8") as file1:
                books = json.load(file1)
            return books
        except json.JSONDecodeError:
            # Handle the case where JSON is invalid
            print("File contains invalid JSON.")
            return {}
        except FileNotFoundError:
            # Handle the case where the file does not exist
            print("File not found.")
            return {}
        except (ValueError, TypeError, IOError) as e:
            print(f"Something went wrong while loading json from file: {e}")
            raise


if __name__ == "__main__":
    user = UserInterface()
    user.add_a_new_book()
    user.display_all_books()
    user.search_books()
    # user.library.borrow_book("11")
    # user.library.return_book("12")
