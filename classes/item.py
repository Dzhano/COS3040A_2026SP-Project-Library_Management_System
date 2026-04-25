from abc import ABC, abstractmethod

from functions import is_valid_date_format, separate_date


class Item(ABC):
    """
    Represents a generic item in the library.
    """
    def __init__(self, id: str = "", name: str = "", description: str = "", 
                 release_date: str = "", reservation_date: str = "", return_date: str = ""):
        # Assigning through setters to trigger validation immediately
        self.id = id
        self.name = name
        self.description = description
        self.type = "Item"
        self.release_date = release_date
        self.reservation_date = reservation_date
        self.return_date = return_date

        self.physical = True  # Default to physical, can be overridden by child classes


    """
    Gets the unique ID of the item. The ID is a string that uniquely identifies the item in the library.
    The ID must be a non-empty string. This ensures that every item can be uniquely identified and prevents issues with empty or invalid IDs
    """
    @property
    def id(self) -> str: # Makes sure the ID is a string and not empty
        return self._id

    @id.setter
    def id(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Item ID must be a non-empty string.")
        self._id = value


    """
    The name of the item.
    While ID is unique and cannot be repeated, the name can be shared among multiple items (e.g., multiple copies of the same book).
    """
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Item name must be a non-empty string.")
        self._name = value

    
    """ The description of the item, which provides additional details about it. """
    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Item description must be a non-empty string.")
        self._description = value


    """ 
    The type of the item, which can be used to distinguish between different categories (e.g., book, DVD).
    It is automatically set by the child classes to reflect the specific type of item they represent.
    """
    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Item type must be a non-empty string.")
        self._type = value


    """ The release date of the item, which indicates when it was made available in the library. """
    @property
    def release_date(self) -> str:
        return self._release_date

    @release_date.setter
    def release_date(self, value: str):
        # For now we will allow future release dates, since it can be used for pre-orders. 
        # We just want to ensure the format is correct.
        if not is_valid_date_format(value):
            raise ValueError("Release date must be in the format MM/DD/YYYY.")
        self._release_date = value


    """ The reservation date of the item, which indicates when it was taken out. """
    @property
    def reservation_date(self) -> str:
        return self._reservation_date
    
    @reservation_date.setter
    def reservation_date(self, value: str):
        if not is_valid_date_format(value):
            raise ValueError("Reservation date must be in the format MM/DD/YYYY.")
        self._reservation_date = value

    
    """ The return date of the item, which indicates when it is due back to the library. """
    @property
    def return_date(self) -> str:
        return self._return_date
    
    @return_date.setter
    def return_date(self, value: str):
        if not is_valid_date_format(value):
            raise ValueError("Return date must be in the format MM/DD/YYYY.")
        self._return_date = value



    def is_physical(self) -> bool:
        """
        Determines if the item is a physical item.
        This method can be overridden by child classes to specify if an item is digital or physical.

        If the item is physical, it returns True. 
        If it's digital, it returns False.
        """
        return self.physical
    
    def __eq__(self, other) -> bool:
        """
        Overloads the equality operator (==) to compare items by their unique ID.
        This allows us to check if two items are the same based on their ID.
        If two items have the same ID, they are considered equal, regardless of their other attributes.
        """
        if not isinstance(other, Item):
            return NotImplemented
        return self.id == other.id

    def is_late(self, current_date: str) -> bool:
        """
        Determines if the item is currently late based on the current date and the return date.
        This method can be overridden by child classes to implement specific late logic for physical and digital items.
        """
        if is_valid_date_format(current_date):
            return_month, return_day, return_year = separate_date(self.return_date)
            current_month, current_day, current_year = separate_date(current_date)
            if current_year < return_year: return False
            elif current_year > return_year: return True
            else:
                if current_month < return_month: return False
                elif current_month > return_month: return True
                else:
                    if current_day <= return_day: return False
                    else: return True
            
        

    @abstractmethod
    def calculate_late_fee(self, days_late: int) -> float:
        """
        Calculates the late fee based on the number of days the item is overdue.
        This is the polymorphic method that must be overridden by child classes.
        """
        pass

    def __str__(self):
        """
        Returns a string representation of the item, including its specific details based on its type. 
        This can be used for displaying item information in a user-friendly format. 
        """
        output = f"Item {self.id} data:\n" 
        output += f"Name: {self.name}\nDescription: {self.description}\nType: {self.type}\n" 
        output += f"Release Date: {self.release_date}\nReservation Date: {self.reservation_date}\nReturn Date: {self.return_date}"
        return output