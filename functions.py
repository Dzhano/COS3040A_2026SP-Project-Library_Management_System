import re

regex = r"^((0[13578]|1[02])\/(0[1-9]|[12][0-9]|3[01])\/((01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20)[0-9]{2}))|((0[469]|11)\/(0[1-9]|[12][0-9]|30)\/(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20)[0-9]{2})|((02)\/(0[1-9]|1[0-9]|2[0-8])\/(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20)[0-9]{2})|((02)\/29\/(((01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20)(04|08|[2468][048]|[13579][26]))|2000))$"


def separate_date(date_string: str):
    """
    Separates a date string into its components (month, day, year).
    Expects the date string to be in the format 'MM/DD/YYYY'
    """
    components = date_string.split('/')

    if len(components) == 3:
        month, day, year = components
        return int(month), int(day), int(year)
    else:
        raise ValueError("Date string must be in the format 'MM/DD/YYYY'")

def is_valid_date_format(date_string: str) -> bool:
    """
    Validates if the provided date string is in the correct format 'MM/DD/YYYY'.
    Uses a regular expression to check the format and validity of the date.
    As well as ensuring that the date is a valid calendar date (e.g., not allowing February 30th).
    """
    date_string = date_string.strip()
    
    try:
        if len(date_string) == 10 and re.match(regex, date_string):
            return True
        else:
            print("The date given for checking is not in the correct format!\n")
            return False
    except ValueError:
        return False

def days_between_two_dates(old_date: str, new_date: str) -> int:
    """
    Calculates the number of days between two dates given in the format 'MM/DD/YYYY'.
    This function assumes that both dates are valid and that the new_date is after the old_date.
    """
    old_month, old_day, old_year = separate_date(old_date)
    new_month, new_day, new_year = separate_date(new_date)

    # Calculate the total number of days for each date
    old_total_days = old_year * 365 + old_month * 30 + old_day
    new_total_days = new_year * 365 + new_month * 30 + new_day

    return new_total_days - old_total_days