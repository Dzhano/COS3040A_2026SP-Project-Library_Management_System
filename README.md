# 📚 Python Library Management System

A comprehensive, object-oriented Library Management System built entirely in Python. This project allows users to load a diverse inventory of media(Books, Ebooks, DVDs, Magazines, and Software), manage library operations via a command-line interface or pre-written script, and export the processed data.

## ✨ Core Features & Grading Criteria

This project was built to fulfill specific advanced programming paradigms:

- **Three-Level Class Hierarchy**: Utilizes an "is-a" inheritance structure (`Item` -> `Physical`/`Electronic` -> `Book`, `DVD`, `Software`, etc.).
- **Strict Encapsulation**: Data integrity is protected using Python `@property` decorators. Setters act as gatekeepers to prevent negative years, empty strings, and invalid date formats (`ValueError`).
- **Polymorphism**: The `calculate_late_fee()` method calculates accumulating percentage-based fees for Physical items, but it calculate flat reinstatement fees for Electronic items.
- **Operator Overloading**: Implements the `__eq__` (`==`) operator to natively compare library objects for exact data duplication.
- **Data Manipulation**: Actively filters, and aggregates collections of objects (e.g., aggregating total late fees owed to the library).
- **Dynamic Configuration**: No hardcoded paths. Uses `config.ini` to dynamically locate I/O files.

## 📂 Project Structure

```text
📦 Project Root
 ┣ 📂 classes/               # Contains all OOP logic
 ┃ ┣ 📜 book.py              
 ┃ ┣ 📜 dvd.py               
 ┃ ┣ 📜 ebook.py             
 ┃ ┣ 📜 electronic.py        # Level 2 Subclass
 ┃ ┣ 📜 item.py              # Level 1 Base Class
 ┃ ┣ 📜 magazine.py          
 ┃ ┣ 📜 physical.py          # Level 2 Subclass
 ┃ ┗ 📜 software.py          
 ┣ 📂 tests/                 # Unit Testing Suite
 ┃ ┣ 📜 __init__.py          # Marks folder as importable module
 ┃ ┣ 📜 test_classes.py      # Tests OOP logic & exceptions
 ┃ ┗ 📜 test_functions.py    # Tests date & math algorithms
 ┣ 📜 config.ini             # System configuration paths
 ┣ 📜 functions.py           # Shared date/math utilities
 ┣ 📜 items.txt              # Text file with the library media input (another file can be picked) 
 ┣ 📜 commands.txt           # Text file with batch commands for auto-execution (another file cannot be used)
 ┗ 📜 main.py                # Main application file
```

### Core System Files
* **`main.py`**: The central engine of the application. It loads configurations, parses the `items.txt` file to instantiate class objects, manages the command-line loop, and handles data exportation.
* **`functions.py`**: A dedicated utility module handling date validation, formatting, and calendar math. This isolates standalone algorithms and prevents circular import dependencies in the main logic.
* **`config.ini`**: A configuration file storing dynamic file paths (like `commands.txt` and `output_data.txt`) to fulfill the requirement of eliminating hard-coded filenames.

### Object-Oriented Classes (`/classes`)
* **`item.py`**: The Level 1 abstract base class. It defines core properties shared by all media, the `is_late()` function, and the overloaded `__eq__` operator.
* **`physical.py`**: A Level 2 subclass representing physical items. Introduces the `Condition` Enum, condition degradation mechanics, and implements accumulating percentage-based late fees.
* **`electronic.py`**: A Level 2 subclass representing digital items. Manages digital license expiration dates and implements flat-rate polymorphic late fees.
* **`book.py`, `dvd.py`, and `magazine.py`**: Level 3 concrete subclasses of `Physical`, featuring unique attributes like `pages`, `director`, and `issue_number`.
* **`ebook.py`, and `software.py`**: Level 3 concrete subclasses of `Electronic`. `Software` introduces a unique `Subscription` tier Enum.

### 🧪 Testing Suite (`/tests`)
* **`test_classes.py`**: The primary unit testing file. Tests OOP logic, polymorphic math, condition degradation, and purposefully feeds bad data (Negative Testing) to ensure `ValueError` exceptions trigger correctly.
* **`test_functions.py`**: Unit tests verifying the accuracy of regex formatting and standalone date math logic.
* **`__init__.py`**: A required empty file that registers the `tests/` folder as a standard Python module, allowing absolute imports to function securely during test discovery.

### 🗄️ Database & Input Files
* **`items.txt`**: The raw database file. Contains comma-separated values acting as the initialization data for the library's inventory.
    * Another file can be picked on its place during the program run.
* **`commands.txt`**: A batch file containing pre-written system commands (e.g., `CalculateLateFee all 03/01/2026`) for automated execution.
    * The file can be skipped if the user decided to write the commands in real-time via the terminal.

## 👨‍💻 Author
**Dzhano Mihaylov**
* Student ID: 200203987
* Course: COS3040A_2026SP Programming in Python
* Professor: Emanuela Mitreva