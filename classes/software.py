from classes.electronic import Electronic
from enum import Enum

class Subscription(Enum):
    Free = 1
    Basic = 2
    Standard = 3
    Premium = 4

class Software(Electronic):
    """
    Represents a software item in the library.
    Inherits from the Electronic class, which represents electronic items in the library.
    """

    def __init__(self, id: str = "", name: str = "", description: str = "", 
                 developer: str = "", username: str = "", subscription: Subscription = Subscription.Free, time: int = 0,
                 release_date: str = "", reservation_date: str = "", return_date: str = "", expiration_date: str = ""):
        super().__init__(id, name, description, release_date, reservation_date, return_date, expiration_date)
        self.developer = developer
        self.username = username
        self.subscription_plan = subscription
        self.usage_time = time # in minutes

        self.type = "Software"  # Set the type to "Software" for this subclass


    @property
    def developer(self) -> str:
        return self._developer
    
    @developer.setter
    def developer(self, value: str):
        self._developer = value

    
    @property
    def username(self) -> str:
        """ Gets the username of the person who rented the software item. """
        return self._username
    
    @username.setter
    def username(self, value: str):
        self._username = value


    @property
    def subscription_plan(self) -> Subscription:
        return self._subscription_plan
    
    @subscription_plan.setter
    def subscription_plan(self, value: Subscription):
        self._subscription_plan = value
    

    @property
    def usage_time(self) -> int:
        # Gets the usage time of the software item in minutes.
        return self._usage_time
    
    @usage_time.setter
    def usage_time(self, value: int):
        self._usage_time = value


    
    def __str__(self):
        return super().__str__() + f"\nDeveloper: {self.developer}\nUsername: {self.username}\nSubscription Plan: {self.subscription_plan.name.title()}\nUsage Time: {self.usage_time} minutes"