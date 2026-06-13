class Book:
    """Represents a book in a library."""

    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._checked_out = False

    def check_out(self) -> str:
        if self._checked_out:
            return f"'{self.title}' is already checked out"
        self._checked_out = True
        return f"Checked out '{self.title}'"

    def return_book(self) -> str:
        if not self._checked_out:
            return f"'{self.title}' is not checked out"
        self._checked_out = False
        return f"Returned '{self.title}'"

    def __repr__(self) -> str:
        status = "available" if not self._checked_out else "checked out"
        return f"Book('{self.title}', status={status})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.isbn == other.isbn

    def __hash__(self) -> int:
        return hash(self.isbn)


class Library:
    """Manages a collection of Book objects."""

    def __init__(self, name: str):
        self.name = name
        self.books: list[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        print(f"Added {book.title} to {self.name}")

    def find_by_author(self, author: str) -> list[Book]:
        return [book for book in self.books if book.author.lower() == author.lower()]

    def available_books(self) -> list[Book]:
        return [book for book in self.books if not book._checked_out]

    def __len__(self) -> int:
        return len(self.books)

    def __repr__(self) -> str:
        return f"Library('{self.name}', {len(self.books)} books)"


def object_interaction_example():
    """Show how objects interact with each other."""
    library = Library("City Library")
    print(f"Created: {library}")

    books = [
        Book("1984", "George Orwell", "978-0451524935"),
        Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084"),
        Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565"),
        Book("Animal Farm", "George Orwell", "978-0451526342"),
    ]

    for book in books:
        library.add_book(book)

    print(f"\nTotal books: {len(library)}")
    print(f"Available: {library.available_books()}")

    print("\n=== Checking Out ===")
    print(books[0].check_out())
    print(books[0].check_out())  # Try again
    print(f"Available after checkout: {library.available_books()}")

    print("\n=== Finding by Author ===")
    orwell_books = library.find_by_author("George Orwell")
    print(f"Books by George Orwell: {orwell_books}")

    print("\n=== Object Equality ===")
    book1 = Book("1984", "George Orwell", "978-0451524935")
    book2 = Book("1984", "George Orwell", "978-0451524935")
    print(f"Same ISBN? {book1 == book2}")

    print("\n=== Returning Book ===")
    print(books[0].return_book())
    print(f"Available after return: {library.available_books()}")


def main():
    object_interaction_example()


if __name__ == "__main__":
    main()
