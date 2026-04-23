from unittest import TestCase, main
from functions import separate_date, is_valid_date_format, days_between_two_dates

class TestFunctions(TestCase):

    def test_separate_date_valid(self):
        """Tests that a valid date string is correctly split into integers."""
        month, day, year = separate_date("12/25/2024")
        self.assertEqual(month, 12)
        self.assertEqual(day, 25)
        self.assertEqual(year, 2024)
        self.assertNotEqual(year, 2025)

    def test_separate_date_invalid(self):
        """Tests that an invalid date string raises a ValueError."""
        with self.assertRaises(ValueError):
            separate_date("12-25-2024") # Wrong separator
        with self.assertRaises(ValueError):
            separate_date("2024")       # Missing parts

    def test_is_valid_date_format(self):
        """Tests the date validation regex and logic."""
        # Positive tests
        self.assertTrue(is_valid_date_format("01/15/2026"))
        self.assertTrue(is_valid_date_format("02/29/2024")) # Leap year valid
        
        # Negative tests
        self.assertFalse(is_valid_date_format("13/01/2026")) # Invalid month
        self.assertFalse(is_valid_date_format("02/30/2026")) # Invalid day
        self.assertFalse(is_valid_date_format("1/5/2026"))   # Missing leading zeros
        self.assertFalse(is_valid_date_format("NotADate"))   # Completely wrong text

    def test_days_between_two_dates(self):
        """Tests the calculation of days between two dates."""
        # Note: Your manual math in functions.py (year*365 + month*30) is an approximation.
        # This test checks if your specific mathematical logic works as written.
        days = days_between_two_dates("01/01/2026", "01/10/2026")
        self.assertEqual(days, 9)

if __name__ == '__main__':
    main()