# validators.py

from datetime import datetime

CATEGORY_MAPPING = {'P': 'personal', 'B': 'business'}
STATUS_MAPPING = {'P': 'Pending', 'IP': 'In Progress', 'C': 'Complete'}

def validate_name():
    """
    Validate task name input.

    Returns:
        str: Valid task name.
    """
    while True:
        try:
            name = input('Enter the task name (or type "quit" to exit): ')
            if name.lower() in ['quit', 'exit']:
                return None
            if not name.strip():
                raise ValueError("Invalid name. Please provide a name, can't be empty.")
            if len(name) < 5:
                raise ValueError('Task name has to have at least 5 characters.')
            return name
        except ValueError as e:
            print(f'Error: {e}')

def validate_date():
    """
    Validate task due date input.

    Returns:
        str: Valid due date in the format DD-MM-YYYY or None if the user exits.
    """
    while True:
        try:
            due_date_str = input("Enter the due date (DD-MM-YYYY) (or type 'quit' to exit): ")
            if due_date_str.lower() in ['quit', 'exit']:
                return None
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
            return due_date.strftime("%d-%m-%Y")
        except ValueError as e:
            print(f'Error: {e}. Please enter the date in the format DD-MM-YYYY.')

def validate_priority():
    """
    Validate task priority input.

    Returns:
        str: Valid priority (low, medium, high) or None if the user exits.
    """
    while True:
        try:
            priority = input('Enter the priority (low, medium, high) (or type "quit" to exit): ').lower()
            if priority.lower() in ['quit', 'exit']:
                return None
            if priority not in ['low', 'medium', 'high']:
                raise ValueError('Invalid option. Priority should be "low", "medium", or "high".')
            return priority
        except ValueError as e:
            print(f'Error: {e}')

def validate_category():
    """
    Validate task category input.

    Returns:
        str: Valid category (P for Personal, B for Business) or None if the user exits.
    """
    while True:
        try:
            category = input('Enter the category: P - (Personal), B - (Business) (or type "quit" to exit): ').upper()
            if category.lower() in ['quit', 'exit']:
                return None
            if len(category) != 1 or category not in ['P', 'B']:
                raise ValueError('Category should be either "P" for Personal or "B" for Business.')
            return category
        except ValueError as e:
            print(f'Error: {e}')

def validate_description():
    """
    Validate task description input.

    Returns:
        str: Valid description (maximum 50 characters) or None if the user exits.
    """
    while True:
        try:
            description = input('Enter the description: (maximum 50 characters, press Enter to skip) (or type "quit" to exit): ')
            if description.lower() in ['quit', 'exit']:
                return None
            if len(description) > 50:
                raise ValueError('Exceeded the input. Maximum characters allowed: 50')
            if not description.strip():
                return ""
            return description
        except ValueError as e:
            print(f'Error: {e}')

def validate_status():
    """
    Validate task status input.

    Returns:
        str: Valid status (C for Complete, P for Pending, IP for In Progress) or None if the user exits.
    """
    while True:
        try:
            status = input('Enter the task status : C - (Complete); P - (Pending);  IP - (In Progress) (or type "quit" to exit): ').upper()
            if status.lower() in ['quit', 'exit']:
                return None
            if status not in ['C', 'P', 'IP']:
                raise ValueError('Status should be C - (Complete); P - (Pending);  IP - (In Progress)')
            return status
        except ValueError as e:
            print(f'Error: {e}')
