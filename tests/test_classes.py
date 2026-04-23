from unittest import TestCase, main
from classes.physical import Condition, condition_from_string
from classes.software import Subscription
from classes.book import Book
from classes.software import Software
from classes.magazine import Magazine
from classes.dvd import DVD
from classes.ebook import Ebook

class TestClasses(TestCase):

    def setUp(self):
        """
        Sets up fresh objects using POSITIONAL arguments to avoid any naming crashes.
        The order matches exactly how you wrote your __init__ functions.
        """
        # Book order: id, name, desc, author, genre, year, pages, release date, reservation date, return date, condition
        self.book1 = Book(
            "B001", "Old Book", "A classic.", "John Doe", "Fiction", 
            1990, 300, "01/01/1990", "01/01/2026", "01/10/2026", Condition.NEW
        )
        
        self.book2 = Book(
            "B002", "New Book", "A modern tale.", "Jane Doe", "Sci-Fi", 
            2020, 250, "05/05/2020", "01/01/2026", "01/15/2026", Condition.GOOD
        )
        
        # Software order: id, name, desc, dev, user, sub, time, release date, reservation date, return date, expiration
        self.software = Software(
            "S001", "Photoshop", "Editor.", "Adobe", "Admin", 
            Subscription.Premium, 60, "01/01/2023", "01/01/2026", "01/05/2026", "12/31/2026"
        )

        # Magazine order: id, name, desc, publisher, issue, release date, reservation date, return date, condition
        self.magazine = Magazine(
            "M001", "NatGeo", "Nature.", "National Geographic", 102, 
            "01/01/2024", "02/01/2026", "02/15/2026", Condition.NEW
        )

        # DVD order: id, name, desc, director, genre, year, duration, release date, reservation date, return date, condition
        self.dvd = DVD(
            "D001", "Inception", "A mind-bending thriller.", "Christopher Nolan", "Sci-Fi",
            2010, 148, "01/01/2024", "02/01/2026", "02/15/2026", Condition.NEW
        )

        # Ebook order: id, name, desc, author, genre, year, pages, release date, reservation date, return date, condition
        self.ebook = Ebook(
            "E001", "Python Programming", "A comprehensive guide.", "John Doe", "Programming",
            2020, 400, "01/01/2024", "02/01/2026", "02/15/2026", "12/31/2026"
        )

    # --- OPERATOR OVERLOADING TESTS ---

    def test_equality_operator(self):
        """Tests the overloaded __eq__ (==) operator."""
        # Create an exact duplicate of book1
        book_copy = Book(
            "B001", "Old Book", "A classic.", "John Doe", "Fiction", 
            1990, 300, "01/01/1990", "01/01/2026", "01/10/2026", Condition.NEW
        )
        
        # book1 should equal the exact copy
        self.assertTrue(self.book1 == book_copy)
        
        # book1 should NOT equal book2
        self.assertFalse(self.book1 == self.book2)


    # --- POLYMORPHISM & CORE LOGIC TESTS ---

    def test_late_fee_physical(self):
        """Tests late fee calculation for Physical items."""
        # book1 was due 01/10/2026. Current date is 01/15/2026 (5 days late).
        # Reserved for 9 days -> $10 fee. Late 5 days -> fee /= 4 -> 10 / 4 = 2.5
        fee = self.book1.calculate_late_fee("01/15/2026")
        self.assertEqual(fee, 2.5)

    def test_late_fee_electronic(self):
        """Tests late fee calculation for Electronic items."""
        # software was due 01/05/2026. Current date is 01/15/2026 (10 days late).
        # Reserved for 4 days -> $3 flat fee.
        fee = self.software.calculate_late_fee("01/15/2026")
        self.assertEqual(fee, 3.0)

    def test_calculate_late_fee_not_late(self):
        """Tests that returning an item early or on time results in a $0 fee."""
        # book1 is due 01/10/2026. Current date is 01/05/2026 (Not late)
        fee = self.book1.calculate_late_fee("01/05/2026")
        self.assertEqual(fee, 0.0)

    def test_is_late_function(self):
        """Tests the calendar math to determine if an item is late."""
        self.assertTrue(self.book1.is_late("01/11/2026"))   # 1 day late
        self.assertFalse(self.book1.is_late("01/05/2026"))  # 5 days early

    def test_string_representations(self):
        """Ensures that printing the objects doesn't crash and returns strings."""
        self.assertIsInstance(str(self.book1), str)
        self.assertIsInstance(str(self.software), str)
        self.assertIsInstance(str(self.magazine), str)
        self.assertIsInstance(str(self.dvd), str)
        self.assertIsInstance(str(self.ebook), str)


    # --- PHYSICAL CONDITION TESTS ---

    def test_is_physical_flag(self):
        """Tests the boolean flag differentiating physical and electronic items."""
        self.assertTrue(self.book1.is_physical())
        self.assertTrue(self.magazine.is_physical())
        self.assertTrue(self.dvd.is_physical())
        
        self.assertFalse(self.software.is_physical())
        self.assertFalse(self.ebook.is_physical())

    def test_degrade_condition(self):
        """Tests the physical item degradation logic."""
        self.assertEqual(self.book1.condition, Condition.NEW)
        
        # Normal degradation pushes it down one tier
        self.book1.degrade_condition()
        self.assertEqual(self.book1.condition, Condition.GOOD)
        
        # Specific degradation jumps straight to target
        self.book1.degrade_condition(Condition.BAD)
        self.assertEqual(self.book1.condition, Condition.BAD)

    def test_gets_stolen(self):
        """Tests the stolen mechanic."""
        self.assertFalse(self.book2.is_stolen())
        self.book2.gets_stolen()
        self.assertTrue(self.book2.is_stolen())
        self.assertEqual(self.book2.condition, Condition.STOLEN)
    
    def test_condition_from_string(self):
        """Tests the helper function that parses text into Condition Enums."""
        self.assertEqual(condition_from_string("NEW"), Condition.NEW)
        self.assertEqual(condition_from_string("good"), Condition.GOOD)
        self.assertEqual(condition_from_string("Average"), Condition.AVERAGE)
        self.assertEqual(condition_from_string("BAD"), Condition.BAD)
        self.assertEqual(condition_from_string("on the verge of collapse"), Condition.ON_THE_VERGE_OF_COLLAPSE)
        self.assertEqual(condition_from_string("Stolen"), Condition.STOLEN)
        
        with self.assertRaises(ValueError):
            condition_from_string("ASHES") # Invalid condition


    # --- NEGATIVE TESTS (ERROR CATCHING) ---

    def test_invalid_base_attributes(self):
        """Tests that the base Item class setters reject empty strings."""
        with self.assertRaises(ValueError):
            self.book1.id = ""
        with self.assertRaises(ValueError):
            self.book1.name = ""

    def test_invalid_dates(self):
        """Tests that setters reject incorrectly formatted dates."""
        with self.assertRaises(ValueError):
            self.book1.release_date = "99/99/9999"  # Fake date
        with self.assertRaises(ValueError):
            self.software.expiration_date = "13/01/2026"  # Month 13 doesn't exist

    def test_invalid_numbers(self):
        """Tests that setters reject negative or invalid numbers."""
        with self.assertRaises(ValueError):
            self.book1.year = -1990  # Year cannot be negative
        with self.assertRaises(ValueError):
            self.book1.pages = -50   # Pages cannot be negative
        with self.assertRaises(ValueError):
            self.magazine.issue_number = -1  # Issue cannot be negative

    def test_invalid_condition_upgrade(self):
        """Tests that you cannot mathematically UPGRADE an item's condition."""
        # book2 starts as GOOD. Trying to force it to NEW should throw a ValueError.
        with self.assertRaises(ValueError):
            self.book2.degrade_condition(Condition.NEW)

if __name__ == '__main__':
    main()