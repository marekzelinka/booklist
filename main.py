import json
import string
from typing import Any

from pydantic import (
    BaseModel,
    PositiveFloat,
    field_validator,
    model_validator,
)


class ISBNMissingError(ValueError):
    """Custom error that is raised when both ISBN10 and ISBN13 are missing."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        super().__init__(message)


class ISBN10FormatError(ValueError):
    """Custom error that is raised when ISBN10 is in invalid format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        super().__init__(message)


class Author(BaseModel):
    name: str
    verified: bool


class Book(BaseModel, frozen=True):
    """Models a book that you can read from a file."""

    title: str
    subtitle: str | None = None
    author: str
    author2: Author | None = None
    publisher: str
    price: PositiveFloat
    isbn_10: str | None = None
    isbn_13: str | None = None

    @model_validator(mode="before")
    @classmethod
    def check_isbn_10_or_13(cls, data: Any) -> Any:
        """Checks that there is either an isbn_10 and/or isbn_13 value defined."""
        if isinstance(data, dict):
            if "isbn_10" not in data and "isbn_13" not in data:
                raise ISBNMissingError(
                    title=data["title"],
                    message="Document should have either an ISBN10 and/or ISBN13.",
                )
        return data

    @field_validator("isbn_10")
    @classmethod
    def isbn_10_valid(cls, value: str) -> str:
        """Checks if the isbn_10 is a valid ISBN."""
        chars = [char for char in value if char in string.digits + "Xx"]
        if len(chars) != 10:
            raise ISBN10FormatError(
                value=value, message="ISBN10 should be 10 character long/"
            )
        if (
            sum(
                (10 - i) * (10 if char in "Xx" else int(char))
                for i, char in enumerate(chars)
            )
            % 11
            != 0
        ):
            raise ISBN10FormatError(
                value=value, message="ISBN10 is invalid ISBN format."
            )
        return value


def main():
    """
    Basic example showing how to read and validate data from a file using Pydantic.
    """

    # read books from json and print
    with open("data.json") as file:
        data = json.load(file)
        books = [Book(**item) for item in data]
        print(books[0])


if __name__ == "__main__":
    main()
