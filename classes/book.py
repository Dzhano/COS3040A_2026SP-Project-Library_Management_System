from classes.physical import Physical
from classes.physical import Condition

class Book(Physical):
    """
    Represents a book in the library.
    Inherits from the Physical class, which represents physical items in the library.
    """

    def __init__(self, item_id: str = "", name: str = "", description: str = "", 
                 author: str = "", genre: str = "", year: int = 2026, pages: int = 0,
                 release_date: str = "", reservation_date: str = "", return_date: str = "", 
                 condition: Condition = Condition.NEW):
        super().__init__(item_id, name, description, release_date, reservation_date, return_date, condition)
        
        self.author = author
        self.genre = genre
        self.year = year
        self.pages = pages

        self.type = "Book"  # Set the type to "Book" for this subclass



    @property
    def author(self) -> str:
        return self._author
    
    @author.setter
    def author(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Author must be a non-empty string.")
        self._author = value


    @property
    def genre(self) -> str:
        return self._genre
    
    @genre.setter
    def genre(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Genre must be a non-empty string.")
        self._genre = value


    @property
    def year(self) -> int:
        return self._year
    
    @year.setter
    def year(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Year must be a positive integer.")
        self._year = value


    @property
    def pages(self) -> int:
        return self._pages
    
    @pages.setter
    def pages(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Pages must be a positive integer.")
        self._pages = value



    def __str__(self):
        return super().__str__() + f"\nAuthor: {self.author}\nGenre: {self.genre}\nYear: {self.year}\nPages: {self.pages}"