import json
from dataclasses import dataclass


@dataclass
class Book:
    """Models a book that you can read from a file."""

    title: str
    subtitle: str
    author: str
    publisher: str
    isbn_10: str
    isbn_13: str
    price: float


def main():
    """
    Basic example showing how to read and validate data from a file using Pydantic.
    """

    # read books from json and print
    with open("data.json") as file:
        data = json.load(file)
        books = [
            Book(
                title=item.get("title", ""),
                subtitle=item.get("subtitle", ""),
                author=item.get("author", ""),
                publisher=item.get("publisher", ""),
                isbn_10=item.get("isbn_10", ""),
                isbn_13=item.get("isbn_13", ""),
                price=item.get("price", 0),
            )
            for item in data
        ]
        print(books[0])


if __name__ == "__main__":
    main()
