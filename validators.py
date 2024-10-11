# validators.py
from colorama import Fore
from datetime import datetime

CATEGORY_MAPPING = {"P": "personal", "B": "business"}
STATUS_MAPPING = {"P": "Pending", "IP": "In Progress", "C": "Complete"}


def validate_name():
    """
    Validate task name input.

    Returns:
        str: Valid task name.
    """
    while True:
        try:
            name = input(
                Fore.CYAN + 'Enter the task name (or type "quit" to exit): '
            )
            if name.lower() in ["quit", "exit"]:
                return None
            if not name.strip():
                raise ValueError(
                    "Invalid name. Please provide a name, can't be empty."
                )
            if len(name) < 5:
                raise ValueError("Task name has to have at least 5 characters.")
            return name
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_date():
    """
    Validate task due date input.

    Returns:
        str: Valid due date in DD-MM-YYYY format.
    """
    while True:
        try:
            due_date_str = input(
                Fore.CYAN
                + "Enter the due date (DD-MM-YYYY) (or type 'quit' to exit): "
            )
            if due_date_str.lower() in ["quit", "exit"]:
                return None
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
            return due_date.strftime("%d-%m-%Y")
        except ValueError as e:
            print(
                Fore.RED
                + f"Error: {e}. Please enter the date in the format DD-MM-YYYY."
            )


def validate_priority():
    """
    Validate task priority input.

    Returns:
        str: Valid priority (low, medium, high).
    """
    while True:
        try:
            priority = input(
                Fore.CYAN
                + 'Enter the priority (low, medium, high) (or type "quit" to exit): '
            ).lower()
            if priority.lower() in ["quit", "exit"]:
                return None
            if priority not in ["low", "medium", "high"]:
                raise ValueError(
                    'Invalid option. Priority should be "low", "medium", or "high".'
                )
            return priority
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_category():
    """
    Validate task category input.

    Returns:
        str: Valid category (P for Personal, B for Business).
    """
    while True:
        try:
            category = input(
                Fore.CYAN
                + 'Enter the category: P - (Personal), B - (Business) (or type "quit" to exit): '
            ).upper()
            if category.lower() in ["quit", "exit"]:
                return None
            if len(category) != 1 or category not in ["P", "B"]:
                raise ValueError(
                    'Category should be either "P" for Personal or "B" for Business.'
                )
            return category
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_description():
    """
    Validate task description input.

    Returns:
        str: Valid description (up to 50 characters).
    """
    while True:
        try:
            description = input(
                Fore.CYAN
                + 'Enter the description: (maximum 50 characters, press Enter to skip) (or type "quit" to exit): '
            )
            if description.lower() in ["quit", "exit"]:
                return None
            if len(description) > 50:
                raise ValueError(
                    "Exceeded the input. Maximum characters allowed: 50"
                )
            if not description.strip():
                return ""
            return description
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_status():
    """
    Validate task status input.

    Returns:
        str: Valid status (C for Complete, P for Pending, IP for In Progress) or None if the user exits.
    """
    while True:
        try:
            status = input(
                Fore.CYAN
                + 'Enter the task status : C - (Complete); P - (Pending); IP - (In Progress) (or type "quit" to exit): '
            ).upper()
            if status.lower() in ["quit", "exit"]:
                return None
            if status not in ["C", "P", "IP"]:
                raise ValueError(
                    "Status should be C - (Complete); P - (Pending); IP - (In Progress)"
                )
            return status
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")
from colorama import Fore  # Ensure you have colorama imported for colored output

def validate_username():
    while True:
        try:
            name = input(Fore.CYAN + 'Enter your Username: ')
            name = name.strip()  # Remove leading/trailing whitespace
            
            # Check if the name is empty
            if not name:
                raise ValueError("Invalid name. Please provide a name, can't be empty.")

            # Check if the length of the name is less than 5
            # Check if the username contains only alphabetic characters
            if not name.isalpha():
                raise ValueError("Username can only contain alphabetic characters.")
            
            if len(name) < 4:
                raise ValueError("Username has to have at least 5 characters.")
        
            return name  # Return the name if validation is successful
            
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

def validate_password():
    while True:
        try:
            password = input("Enter your password: ").strip()
            if len(password) < 5:
                raise ValueError("For better security, the password must have at least 5 characters.")
            return password
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

def validate_login_password():
    while True:
        try:
            password = input("Enter your password: ").strip()
            if not password:
                raise ValueError("Password cannot be empty.")
            return password
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

