from classes.physical import Physical
from classes.physical import Condition

class Magazine(Physical):
    """
    Represents a magazine in the library.
    Inherits from the Physical class, which represents physical items in the library.
    """

    def __init__(self, id: str = "", name: str = "", description: str = "", 
                 publisher: str = "", issue_number: int = 0,
                 release_date: str = "", reservation_date: str = "", return_date: str = "", 
                 condition: Condition = Condition.NEW):
        super().__init__(id, name, description, release_date, reservation_date, return_date, condition)
        
        self.publisher = publisher
        self.issue_number = issue_number

        self.type = "Magazine"  # Set the type to "Magazine" for this subclass



    @property
    def publisher(self) -> str:
        return self._publisher
    
    @publisher.setter
    def publisher(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Publisher must be a non-empty string.")
        self._publisher = value


    @property
    def issue_number(self) -> int:
        return self._issue_number
    
    @issue_number.setter
    def issue_number(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Issue number must be a positive integer.")
        self._issue_number = value

    

    def __str__(self):
        return super().__str__() + f"\nPublisher: {self.publisher}\nIssue Number: {self.issue_number}"