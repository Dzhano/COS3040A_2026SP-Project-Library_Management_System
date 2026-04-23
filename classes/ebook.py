from classes.electronic import Electronic

class Ebook(Electronic):
    """
    Represents a book in the library.
    Inherits from the Physical class, which represents electronic items in the library.
    """

    def __init__(self, id: str = "", name: str = "", description: str = "",
                  author: str = "", genre: str = "", year: int = 2026, size: int = 0,
                  release_date: str = "", reservation_date: str = "", return_date: str = "", 
                  expiration_date: str = ""): 
        super().__init__(id, name, description, release_date, reservation_date, return_date, expiration_date)
        
        self.author = author
        self.genre = genre
        self.year = year
        self.size = size # in MB

        self.type = "Ebook"  # Set the type to "Ebook" for this subclass



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
    def size(self) -> int:
        return self._size
    @size.setter
    def size(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Size must be a positive integer.")
        self._size = value

    
    def __str__(self):
        return super().__str__() + f"\nAuthor: {self.author}\nGenre: {self.genre}\nYear: {self.year}\nSize: {self.size}MB"