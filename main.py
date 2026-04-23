import os, csv, sys

from functions import is_valid_date_format

from classes.physical import Physical, Condition
from classes.book import Book
from classes.magazine import Magazine
from classes.software import Software
from classes.dvd import DVD
from classes.electronic import Electronic
from classes.ebook import Ebook
from classes.software import Subscription

ids = set()  # To track unique IDs

def parse_item_line(line: str):
    # Parses a line from the .txt file and returns the corresponding Item object.
    
    try:
        # Remove any trailing comments on the line (e.g., "# Failed years")
        if "#" in line:
            line = line.split("#")[0]
            
        line = line.strip()
        if not line:
            return None

        # Use csv to safely parse the line, respecting commas inside quotes
        reader = csv.reader([line], skipinitialspace=True)
        parts = next(reader)
        
        # The first element is always the item type
        item_type = parts[0]
        
        # Every item shares these first 4 properties based on the items.txt format
        name = parts[1]
        description = parts[3]

        item_id = parts[2]
        if item_id in ids:
            print(f"Warning: Duplicate ID '{item_id}' found for item '{name}'. Skipping this item.")
            return None
    except Exception as e:
        print("Error details: ", e)
        return None
    
    # Helper dictionary to safely map text conditions to the Enum
    condition_map = {
        "NEW": Condition.NEW,
        "GOOD": Condition.GOOD,
        "AVERAGE": Condition.AVERAGE,
        "BAD": Condition.BAD,
        "ON THE VERGE OF COLLAPSE": Condition.ON_THE_VERGE_OF_COLLAPSE,
        "STOLEN": Condition.STOLEN
    }

    try:
        if item_type == "Book" or item_type == "Ebook":
            # Book/Ebook format: Book/Ebook, "name", ID, "description", author, genre, year, pages/size, release_date, reservation_date, return_date, condition/expirationDate
            author, genre, year, pages, release_date, reservation_date, return_date, condition_str = parts[4:12]

            if item_type == "Book":
                condition = condition_map.get(condition_str.upper().strip(), Condition.NEW)
                return Book(item_id, name, description, author, genre, int(year), int(pages), release_date, reservation_date, return_date, condition)
            elif item_type == "Ebook":
                return Ebook(item_id, name, description, author, genre, int(year), int(pages), release_date, reservation_date, return_date, condition_str)
        
        elif item_type == "DVD":
            # DVD format: DVD, "name", ID, "description", director, genre, year, duration, release_date, reservation_date, return_date, condition
            director, genre, year, duration, release_date, reservation_date, return_date, condition_str = parts[4:12]
            condition = condition_map.get(condition_str.upper().strip(), Condition.NEW)
            return DVD(item_id, name, description, director, genre, int(year), int(duration), release_date, reservation_date, return_date, condition)

        elif item_type == "Magazine":
            # Magazine format: Magazine, "name", ID, "description", publisher, issue_number, release_date, reservation_date, return_date, condition
            publisher, issue_num, release_date, reservation_date, return_date, cond_str = parts[4:10]
            condition = condition_map.get(cond_str.upper().strip(), Condition.NEW)
            return Magazine(item_id, name, description, publisher, int(issue_num), release_date, reservation_date, return_date, condition)

        elif item_type == "Software":
            # Software format: Software, "name", ID, "description", "developer" username, subscription_plan, usage_time, release_date, reservation_date, return_date, expirationDate
            developer, username, subscription_str, usage_time, release_date, reservation_date, return_date, expiration_date = parts[4:12]
            
            # Convert Subscription string to Enum safely
            subscription = getattr(Subscription, subscription_str.strip().title(), Subscription.Free)
            
            return Software(item_id, name, description, developer, username, subscription, int(usage_time), release_date, reservation_date, return_date, expiration_date)

        else:
            print(f"Warning: Unknown item type '{item_type}' skipped.")
            return None

    except Exception as e:
        # If the user put a bad date, or didn't supply enough arguments, it catches it here
        print(f"Failed to parse item [{name}]: {e}")
        return None
    
def process_command(input_command: str):
    command = input_command.strip().split()
    if not command: return True

    if command[0] == "GetsStolen":
        target = command[1] if len(command) > 1 else "all"
        count = 0
        for item in items:
            if isinstance(item, Physical):  # Only physical items can be stolen
                if target == "all" or item.id == target:
                    item.gets_stolen()
                    count += 1
        print(f"Marked {count} physical item(s) as stolen.\n")
    
    elif command[0] == "DegradeCondition":
        target = command[1] if len(command) > 1 else "all"
        # Check if a specific condition was provided (e.g., ./BAD)
        condition = None
        if len(command) > 2 and not command[2].startswith("."):
            condition_str = command[2].upper()
            try:
                condition = Condition[condition_str]
            except KeyError:
                print(f"Warning: '{condition_str}' is not a valid condition.\n")
                return True

        count = 0
        for item in items:
            if isinstance(item, Physical):
                if target == "all" or item.id == target:
                    try:
                        item.degrade_condition(condition)
                        count += 1
                    except ValueError as e:
                        print(f"Could not degrade item {item.id}: {e}")
        print(f"Degraded condition for {count} physical item(s).\n")
    
    elif command[0] == "CalculateLateFee": 
        if len(command) < 3:
            print("Usage: CalculateLateFee {ID}/all {MM/DD/YYYY}\n")
            return True
        
        target = command[1]
        date_str = command[2]

        if not is_valid_date_format(date_str):
            return True

        total_fee = 0.0
        for item in items:
            if target == "all" or item.id == target:
                # POLYMORPHISM: This calls the specific calculate_late_fee method 
                # depending on whether it is Physical or Electronic!
                fee = item.calculate_late_fee(date_str)
                total_fee += fee
                if target != "all":
                    print(f"Late fee for {item.name}: ${fee:.2f}")
        
        if target == "all":
            # AGGREGATION: We aggregated all the fees into a single total
            print(f"Total Late Fees owed to the library: ${total_fee:.2f}\n")
    
    elif command[0] == "GetCodeExpirationDate":
        target = command[1] if len(command) > 1 else "all"
        for item in items:
            if isinstance(item, Electronic):
                if target == "all" or item.id == target:
                    print(f"Code Expiration for [{item.id}] {item.name}: {item.expiration_date}")
        print("\n")
    
    elif command[0] == "CheckIfLate":
        if len(command) < 2:
            print("Usage: CheckIfLate {MM/DD/YYYY}\n")
            return True
        
        date_str = command[1]
        if not is_valid_date_format(date_str):
            return True
        
        late_count = 0
        for item in items:
            if item.is_late(date_str):
                print(f"LATE: {item.name} (ID: {item.id}) - Was due on {item.return_date}")
                late_count += 1
        if late_count == 0:
            print("Great news! No items are currently late.")
        print('\n')
   
    elif command[0] == "Display" or command[0] == "Show":
        # DATA FILTERING
        target_type = command[1] if len(command) > 1 else "all"
        filtered_items = []
        
        late_date = ""
        if target_type == "late":
            late_date = input("For which date (MM/DD/YYYY): ")

        for item in items:
            if target_type in ["all", "everything"]:
                filtered_items.append(item)
            elif target_type == "physicals" and isinstance(item, Physical):
                filtered_items.append(item)
            elif target_type == "electronics" and isinstance(item, Electronic):
                filtered_items.append(item)
            elif target_type == "books" and item.type == "Book":
                filtered_items.append(item)
            elif target_type == "DVDs" and item.type == "DVD":
                filtered_items.append(item)
            elif target_type == "magazines" and item.type == "Magazine":
                filtered_items.append(item)
            elif target_type == "ebooks" and item.type == "Ebook":
                filtered_items.append(item)
            elif target_type == "softwares" and item.type == "Software":
                filtered_items.append(item)
            elif target_type == "late":
                if item.is_late(late_date):
                    filtered_items.append(item)
        
        print(f"\n--- Displaying: {target_type} ---")
        if not filtered_items:
            print("No items found matching this criteria.")
        else:
            for item in filtered_items:
                print(item)
                print("\n")
        print("-" * 35 + "\n")
    
    elif command[0] == "Show" and len(command) > 1 and command[1] == "commands":
        print(command_message)
    
    else:
        print(f"The command {input_command.strip()} is not valid. Please try again.\n")

if __name__ == "__main__":
    print("Welcome to our library program! Here you can upload the collection of items contained in your library.")
    print("In order to add items to the system you need to fill the \"items.txt\" file with the information regarding each physical and electronical item or put your file following the following instructions.")
    print("WARNING! Read the instructions beforehand in the above mentioned \"items.txt\" file to avoid any unnecessary program exceptions. Also, please fill an appropriate data (no negative years, unallowed conditions, etc.).")
    print("\nThank you for buying our program!")
    print("If there are any problems, feel free to contact our support team :)\n")

    file_choice = ""
    while file_choice not in ["items.txt", "another"]:
        file_choice = input("What file would you want to use? \"items.txt\" or another? Answer explicitly: ")
    
    if file_choice == "another":
        file_choice = input("Please enter the location of the file with all of the necessary parts. Including slashes (/) if the file is not in the same folder as \"items.txt\". As well as the \".txt\" so that it can be read by the program.\nFile: ")
        choice = "No"

        while True:
            choice = input("Are you sure this is the file you want to use? Yes or No (answer explicitly, if you do not, the program will ask you again): ")
            if choice == "Yes": break
            if choice == "No":
                file_choice = input("Enter the file name again: ")

    items = []

    try:
        with open(file_choice, "r") as items_file:
            os.system('cls' if os.name == 'nt' else 'clear')
            for line in items_file:
                line = line.strip()
                # Skip blank lines and lines that start with #
                if not line or line.startswith("#"):
                    continue
                
                # Parse the line into an Object
                new_item = parse_item_line(line)
                
                if new_item is not None:
                    ids.add(new_item.id)  # Add the ID to the set of seen IDs
                    items.append(new_item)

    except FileNotFoundError:
        print("\nIt seems that the file you entered does not exist. Please try again by adding/creating the file before running the next program.")
        sys.exit()
    except UnicodeDecodeError as e:
        print("\nThe file you choose failed to open. Please try again in the next program running.")
        print("Please read the instructions again before you choose a file!")
        print("If everything seems to be fine, then the problem may be from the file itself - it can be broken, corrupted or has another problem.")
        print("Please check everything again.")
        print("Error details: ", e)
        sys.exit()
    except Exception as e:
        print("Error details: ", e)
        sys.exit()

    print("\nHow would you like to send commands to the program?")
    print("With the \"commands.txt\" file (beforehand prepared) or from the command window directly (at the moment)?")
    command_option = input("Answer explicitly: \"File\" or \"Window\": ")
    while command_option != "File" and command_option != "Window":
        command_option = input("Please select \"File\" or \"Window\": ")
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if command_option == "File":
        with open("commands.txt", "r") as commands_file:
            if commands_file.closed:
                print("\nThe file you choose failed to open. Please try again in the next program running.")
                print("Please read the instructions again before you choose a file!")
                print("If everything seems to be fine, then the problem may be from the file itself - it can be broken, corrupted or has another problem.")
                print("Please check everything again.")
            else:
                while commands_file:
                    line = commands_file.readline()
                    if not line: break
                    
                    if line.startswith("#"): continue
                    if line.__contains__("End program"): break
                    process_command(line)
    
    elif command_option == "Window":
        command_message = "\nYou can enter the following types of commands:\n\n"
        command_message += "\"CheckIfLate {MM/DD/YYYY}\" - checks whether each item is late depending on the provided date\n"
        command_message += "\"DegradeCondition all/{specific ID} ./{type of Condition}\" - degrades the condition of a specific physical item or all of them\n"
        command_message += "\"CalculateLateFee {specific ID}/all {MM/DD/YYYY}\" - calculates the late fee of a specific item or all of them\n"
        command_message += "\"GetCodeExpirationDate {specific ID}/all\" - gets the expiration date of the electronic item(s) code after which it won't work anymore\n"
        command_message += "\"GetsStolen {specific ID}/all\" - a specific physical item or all of them are considered stolen from the library\n"
        command_message += "\"Display physicals / electronics / books / ebooks / magazines / DVDs / softwares / late / all / everything\" - displays on the command window the desired output of data\n"
        command_message += "\"Show physicals / electronics / books / ebooks / magazines / DVDs / softwares / late / all / everything\" - displays on the command window the desired output of data\n\n"
        command_message += "\"Show commands\" - display the current commands again. Useful if you do not want to scroll all the way up to see what functions you can do.\n"
        command_message += "\"End program\" - stops the acceptance of new commands\n"
        command_message += "Anything else written will not be accepted and the program will ask you for a new commands without doing anything beforehand.\n\n"
        print(command_message)
        
        while True:
            command = input("Enter a command: ")
            if command =="End program": break
            elif command == "Show commands":
                print(command_message)
            else: process_command(command)
    
    exporting = input("Would you want to export the items' data in another file? Yes or No (answer explicitly - if not, it will be considered as \"No\"): ")

    if exporting == "Yes":
        try:
            with open("output_data.txt", "w") as output_file:
                if output_file.closed:
                    print("\nThe file you choose failed to be created. Please try again in the next program running.")
                    print("Please read the instructions again before you choose a file!")
                    print("If everything seems to be fine, then the problem may be from the file itself - it can be broken, corrupted or has another problem.")
                    print("Please check everything again.")
                for item in items:
                    output_file.write(item.__str__() + "\n\n")

                    """ # If we want the data to be a bit more organized.
                    counter = 1 # Add it before the loop
                    output_file.write("Item " + str(counter) + ":\n")
                    output_file.write("ID: " + item.id + "\n")
                    output_file.write("Name: " + item.name + "\n")
                    output_file.write("Type: " + item.type + "\n")
                    output_file.write("Description: " + item.description + "\n")

                    if item.type == "Book":
                        output_file.write("Author: " + item.author + "\n")
                        output_file.write("Genre: " + item.genre + "\n")
                        output_file.write("Year: " + str(item.year) + "\n")
                        output_file.write("Pages: " + str(item.pages) + "\n")
                        output_file.write("Physical condition: " + item.get_physical_condition() + "\n")
                    elif item.type == "Ebook":
                        output_file.write("Author: " + item.author + "\n")
                        output_file.write("Genre: " + item.genre + "\n")
                        output_file.write("Year: " + str(item.year) + "\n")
                        output_file.write("Size: " + str(item.size) + "\n")
                        output_file.write("Digital code's expiration date: " + item.expiration_date + "\n")
                    elif item.type == "Magazine":
                        output_file.write("Publisher: " + item.publisher + "\n")
                        output_file.write("Issue number: " + str(item.issue_number) + "\n")
                        output_file.write("Physical condition: " + item.get_physical_condition() + "\n")
                    elif item.type == "DVD":
                        output_file.write("Director: " + item.director + "\n")
                        output_file.write("Genre: " + item.genre + "\n")
                        output_file.write("Year: " + str(item.year) + "\n")
                        output_file.write("Duration: " + str(item.duration) + " minutes\n")
                        output_file.write("Physical condition: " + item.get_physical_condition() + "\n")
                    elif item.type == "Software":
                        output_file.write("Developer: " + item.developer + "\n")
                        output_file.write("Username: " + item.username + "\n")
                        output_file.write("Subscription Plan: " + item.get_subscription_plan() + "\n")
                        output_file.write("Usage Time: " + str(item.usage_time) + " minutes\n")
                        output_file.write("Digital code's expiration date: " + item.expiration_date + "\n")

                    output_file.write("Release Date: " + item.release_date + "\n")
                    output_file.write("Reservation Date: " + item.reservation_date + "\n")
                    output_file.write("Return Date: " + item.return_date + "\n\n")
                    
                    counter += 1
                    """

        except Exception as e:
            print("Exporting failed. Error details: ", e)

    items.clear()
    ending_message = "\nThank you for using my program! Have a great day!\n"
    ending_message += "Creator: Dzhano Mihaylov\n"
    ending_message += "Student ID: 200203987\n"
    ending_message += "Course: COS3040A_2026SP Programming in Python\n"
    ending_message += "Professor: Emanuela Mitreva\n"
    print(ending_message)