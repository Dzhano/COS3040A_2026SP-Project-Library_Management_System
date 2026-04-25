from abc import ABC

from functions import days_between_two_dates, is_valid_date_format
from classes.item import Item


class Electronic(Item, ABC):
    """
    Represents an electronic or digital item in the library.
    Inherits from the abstract Item class.
    """

    def __init__(self, id: str = "", name: str = "", description: str = "", 
                 release_date: str = "", reservation_date: str = "", return_date: str = "", expiration_date: str = ""):
        super().__init__(id, name, description, release_date, reservation_date, return_date)
        self.type = "Electronic"
        self.expiration_date = expiration_date
        self.physical = False  # Explicitly set physical to False for this subclass


    """ The expiration date for electronic items that indicates when the license for the software or digital content will expire. """
    @property
    def expiration_date(self) -> str:
        # Gets the license expiration date.
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value: str):
        if not is_valid_date_format(value):
            raise ValueError("Expiration date must be in the format MM/DD/YYYY.")
        self._expiration_date = value


    def calculate_late_fee(self, current_date: str) -> float:
        """
        Calculates the late fee for an electronic item.
        Electronic items often have a flat fee to reinstate a revoked license, 
        rather than a daily accumulating fee.
        """
        fee = 0.0

        if self.is_late(current_date):
            # Depending on for how long the program was reserved for, the bigger the tax will be for not returning it.
            days_during_reservation = days_between_two_dates(self.reservation_date, self.return_date)
            if days_during_reservation <= 7: fee = 3 # $3
            elif days_during_reservation <= 14: fee = 7 # $7
            elif days_during_reservation <= 28: fee = 15 # $15
            elif days_during_reservation <= 40: fee = 25 # $25
            else: fee = 40 # $40

            # Depending on how long the program has not been return for, the closer the tax rate to the initial will be.
            days_late = days_between_two_dates(self.return_date, current_date)
            if days_late <= 2: fee = 0 # No fee at all assuming that the software is returned quickly.
        else: 
            print(f"The {self.type} {self.name} is not late, no fee applies.")
        return fee

    def __str__(self):
        return super().__str__() + f"\nExpiration Date: {self.expiration_date}"