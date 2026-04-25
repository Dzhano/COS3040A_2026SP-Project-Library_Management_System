from classes.physical import Physical
from classes.physical import Condition

class DVD(Physical):
    """
    Represents a DVD item in the library.
    Inherits from the Physical class.
    It can also be classified as an electronic item, 
    but for the sake of this project, we will treat it as a physical item 
    due to it having a physical box and disc and the fact that it can be damaged or stolen.
    """

    def __init__(self, id: str = "", name: str = "", description: str = "", 
                 director: str = "", genre: str = "", year: int = 2026, duration: int = 0,
                 release_date: str = "", reservation_date: str = "", return_date: str = "", 
                 condition: Condition = Condition.NEW):
        super().__init__(id, name, description, release_date, reservation_date, return_date, condition)
        self.type = "DVD"
        self.director = director
        self.genre = genre
        self.year = year
        self.duration = duration # in minutes



    """ The name of the director of the DVD. """
    @property
    def director(self) -> str:
        return self._director
    
    @director.setter
    def director(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Director must be a non-empty string.")
        self._director = value

    
    """ The genre of the DVD. It can be any type - action, comedy, horror, etc. """
    @property
    def genre(self) -> str:
        return self._genre
    
    @genre.setter
    def genre(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Genre must be a non-empty string.")
        self._genre = value

    
    """ The year the DVD was released. Not the movie, but the physical DVD itself. """
    @property
    def year(self) -> int:
        return self._year
    
    @year.setter
    def year(self, value: int):
        if not isinstance(value, int) or value < 1888: # The first film was made in 1888
            raise ValueError("Year must be an integer greater than or equal to 1888.")
        self._year = value
    

    """ The duration of the DVD in minutes. """
    @property
    def duration(self) -> int:
        return self._duration
    
    @duration.setter
    def duration(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Duration must be a non-negative integer.")
        self._duration = value
    


    def __str__(self):
        return super().__str__() + f"\nDirector: {self.director}\nGenre: {self.genre}\nYear: {self.year}\nDuration: {self.duration} minutes"