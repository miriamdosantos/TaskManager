# validators.py
from colorama import Fore
import pwinput
from datetime import datetime


def validate_name(
    prompt_message="Enter the task name (or type 'quit' to exit): ",
):
    """
    Validate task name input with a custom prompt message.

    Parameters:
        prompt_message (str): The message displayed when asking for input.

    Returns:
        str: Valid task name, or None if the user types 'quit'.
    """
    while True:
        try:
            name = input(Fore.CYAN + prompt_message)
            if not name.strip():
                raise ValueError(
                    "Invalid name. Please provide a name, can't be empty."
                )
            if name.lower() == "quit":
                return None
            if len(name) < 5:
                raise ValueError(
                    "Task name has to have at least 5 characters."
                )
            if name.isnumeric():
                raise ValueError("Task name cannot be only numeric.")
            return name
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_date(
    prompt_message="Enter the due date (DD-MM-YYYY) (or type 'quit' to exit): ",
):
    """
    Validate task due date input.

    Returns:
        str: Valid due date in DD-MM-YYYY format, or None if the user quits.
    """
    while True:
        try:
            due_date_str = input(Fore.CYAN + prompt_message)
            if not due_date_str.strip():
                raise ValueError(
                    "Invalid date. Please provide a date, it can't be empty."
                )
            if due_date_str.lower() == "quit":
                return None

            # Parse the input date and compare with today's date
            due_date = datetime.strptime(
                due_date_str, "%d-%m-%Y"
            ).date()
            today = datetime.now().date()

            # Check if the due date is in the past
            if due_date < today:
                print(
                    Fore.RED
                    + f"Invalid date: {due_date_str} has already passed."
                )
                continue  # Prompt the user again for a valid date

            # Return the date in the requested format if it's valid
            return due_date.strftime("%d-%m-%Y")

        except ValueError:
            print(
                Fore.RED
                + " Please enter the date in the format DD-MM-YYYY."
            )


def validate_priority(
    prompt_message='Enter the priority (low, medium, high) (or type "quit" to exit): ',
):
    """
    Validate task priority input.

    Returns:
        str: Valid priority (low, medium, high).
    """
    while True:
        try:
            priority = input(Fore.CYAN + prompt_message).lower()
            if not priority.strip():
                raise ValueError(
                    "Invalid priority. Please provide a priority, it can't be empty."
                )
            if priority.lower() in "quit":
                return None
            if priority not in ["low", "medium", "high"]:
                raise ValueError(
                    'Invalid option. Priority should be "low", "medium", or "high".'
                )
            return priority
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_category(
    prompt_message='Enter the category: P - (Personal), B - (Business) (or type "quit" to exit): ',
):
    """
    Validate task category input.

    Returns:
        str: Valid category (P for Personal, B for Business).
    """
    while True:
        try:
            category = input(Fore.CYAN + prompt_message).upper()
            if not category.strip():
                raise ValueError(
                    "Invalid category. Please provide a category, it can't be empty."
                )
            if category.lower() in "quit":
                return None
            if category not in ["P", "B"]:
                raise ValueError(
                    'Category should be either "P" for Personal or "B" for Business.'
                )
            if category == "P":
                return "Personal"
            elif category == "B":
                return "Business"
            return category
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_description(
    prompt_message='Enter the description: (maximum 300 characters, press Enter to "skip" or type "quit" to exit): ',
):
    """
    Validate task description input.

    Returns:
        str: Valid description (up to 300 characters).
    """
    while True:
        try:
            description = input(Fore.CYAN + prompt_message)
            if not description.strip():
                return ""
            if description.lower() in ["quit", "exit"]:
                return None
            if len(description) > 300:
                raise ValueError(
                    f"{Fore.RED}Exceeded the input. Maximum characters allowed: 50"
                )

            return description
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_status(
    prompt_message='Enter the task status : C - (Complete); P - (Pending); IP - (In Progress) (or type "quit" to exit): ',
):
    """
    Validate task status input.

    Returns:
        str: Valid status (C for Complete, P for Pending, IP for In Progress) or None if the user exits.
    """
    while True:
        try:
            status = input(Fore.CYAN + prompt_message).upper()
            if not status.strip():
                raise ValueError(
                    f"{Fore.RED}Invalid status. Please provide a status, it can't be empty."
                )
            if status.lower() in "quit":
                return None
            if status not in ["C", "P", "IP"]:
                raise ValueError(
                    "Status should be C - (Complete); P - (Pending); IP - (In Progress)"
                )
            if status == "P":
                return "Pending"
            elif status == "C":
                return "Complete"
            elif status == "IP":
                return "In Progress"
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_username():
    while True:
        try:
            name = input(Fore.CYAN + "Enter your Username: ")
            name = name.strip()  # Remove leading/trailing whitespace

            # Check if the name is empty
            if not name:
                raise ValueError(
                    "Invalid name. Please provide a name, can't be empty."
                )

            # Check if the length of the name is less than 5
            # Check if the username contains only alphabetic characters
            if not name.isalpha():
                raise ValueError(
                    "Username can only contain alphabetic characters."
                )

            if len(name) < 4:
                raise ValueError(
                    "Username has to have at least 5 characters."
                )

            return name  # Return the name if validation is successful

        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_password():
    while True:
        try:
            # Use pwinput with mask='*' to show asterisks
            password = pwinput.pwinput(
                prompt="Enter your password: ", mask="*"
            ).strip()
            if len(password) < 5:
                raise ValueError(
                    "For better security, the password must have at least 5 characters."
                )
            return password
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")


def validate_login_password():
    while True:
        try:
            # Use pwinput with mask='*' to show asterisks
            password = pwinput.pwinput(
                prompt="Enter your password: ", mask="*"
            ).strip()
            if not password:
                raise ValueError("Password cannot be empty.")
            return password
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")
