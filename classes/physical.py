from abc import ABC
from enum import Enum

from functions import days_between_two_dates
from classes.item import Item

class Condition(Enum):
    """ 
    Represents the physical condition of an item. 
    The quality of a physical item can degrade over time, and this enum helps to track that. 
    """
    NEW = 1
    GOOD = 2
    AVERAGE = 3
    BAD = 4
    ON_THE_VERGE_OF_COLLAPSE = 5
    STOLEN = 6

def condition_from_string(condition_str: str) -> Condition:
    condition_str = condition_str.strip().upper().replace(" ", "_")
    try:
        return Condition[condition_str]
    except KeyError:
        raise ValueError(f"Invalid condition: {condition_str}. Valid conditions are: {[c.name for c in Condition]}")
    
class Physical(Item, ABC):
    """
    Represents a physical item in the library.
    Inherits from the abstract Item class.
    """

    def __init__(self, id: str, name: str, description: str, 
                 release_date: str, reservation_date: str, return_date: str, 
                 condition: Condition):
        super().__init__(id, name, description, release_date, reservation_date, return_date)
        self.type = "Physical"
        self.condition = condition
        self.physical = True  # Explicitly set physical to True for this subclass

    """ The physical condition of the item. It takes from the Condition enum. """
    @property
    def condition(self) -> Condition:
        return self._condition

    @condition.setter
    def condition(self, value: Condition):
        self._condition = value

    def degrade_condition(self, condition: Condition | None = None):
        """
        Degrades the condition of the physical item to the next worst state.
        If the item is already 'On the verge of collapse' or 'Stolen', it does not degrade further.
        """
        if condition is None: # In case no specific condition is provided, degrade to the next worse state
            if self._condition == Condition.NEW:
                self._condition = Condition.GOOD
            elif self._condition == Condition.GOOD:
                self._condition = Condition.AVERAGE
            elif self._condition == Condition.AVERAGE:
                self._condition = Condition.BAD
            elif self._condition == Condition.BAD:
                self._condition = Condition.ON_THE_VERGE_OF_COLLAPSE
        
        else: # If a specific condition is provided, degrade to that condition if it's worse than the current condition
            if self._condition.value < condition.value:
                self._condition = condition
            else:
                raise ValueError("New condition must be worse than the current condition.")
    
    def gets_stolen(self):
        """ Marks the item as stolen, which is the worst condition. It cannot be degraded further or marked as not stolen (another condition). """
        self._condition = Condition.STOLEN
    
    def is_stolen(self) -> bool:
        """ Checks if the item is marked as stolen. """
        return self._condition == Condition.STOLEN

    def calculate_late_fee(self, current_date: str) -> float:
        """
        Calculates the late fee for a physical item.
        Physical items accumulate fees steadily based on days late.
        """
        fee = 0.0

        if self.is_late(current_date):
            # Depending on for how long the item was reserved for, the bigger the tax will be for not returning it.
            days_during_reservation = days_between_two_dates(self.reservation_date, self.return_date)
            if days_during_reservation <= 7: fee = 5 # $5
            elif days_during_reservation <= 14: fee = 10 # $10
            elif days_during_reservation <= 28: fee = 25 # $25
            elif days_during_reservation <= 40: fee = 40 # $40
            else: fee = 55 # $55

            # Depending on how long the item has not been return for, the closer the tax rate to the initial will be.
            days_late = days_between_two_dates(self.return_date, current_date)
            if days_late <= 2: fee = 0 # No fee for the first 2 days late
            elif days_late <= 5: fee /= 4 # A quarter of the fee
            elif days_late <= 7: fee /= 3 # A third of the fee
            elif days_late <= 10: fee /= 2 # Half of the fee
            # After 10 days late, the full fee applies
        else: 
            print(f"The {self.type} {self.name} is not late, no fee applies.")
        return fee

    def __str__(self) -> str:
        return super().__str__() + f"\nPhysical Condition: {self._condition.name.replace("_", " ").title()}"