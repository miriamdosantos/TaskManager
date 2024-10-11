from google_sheets import load_data_from_sheet, save_data_to_sheet, setup_google_sheets
from colorama import Fore, init
from validators import validate_username, validate_login_password, validate_password
import bcrypt

# Initialize colorama for text formatting
init(autoreset=True)

def register_user(users_data):
    """
    Registers a new user in the system.

    Args:
        users_data (dict): Dictionary containing all user data.
        
    Returns:
        str: The username of the newly registered user, or None if registration failed.
    """
    username = validate_username()
    
    # Check if username already exists
    while True:
        if username in users_data:
            print(f"{Fore.RED}Username already exists.")
            username = validate_username()
        else:
            break
        
    # Validate and hash the user's password
    password = validate_password()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Add the new user to the users_data dictionary
    users_data[username] = {
        "password": hashed_password,
        "tasks": {
            "personal": [],
            "business": []
        }
    }
    
    print(f"{Fore.GREEN}User registered successfully.")
    save_data_to_sheet(users_data)  # Save user data to Google Sheets
    return username  # Return username if registration was successful


def login(users_data):
    """
    Handles user login by validating the username and password.

    Args:
        users_data (dict): Dictionary containing all user data.
    
    Returns:
        str: The username of the logged-in user, or None if login failed.
    """
    username = validate_username()
    input_password = validate_login_password()
    
    # Retrieve the stored password for the provided username
    stored_password = users_data.get(username, {}).get('password', None)
    
    # Check if the username exists
    if not stored_password:
        print(f"{Fore.RED}Username not found.")
        return None  # Return None if username doesn't exist
    
    # Check if the input password matches the stored hashed password
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8')):
        print(f"{Fore.GREEN}Login successful!")
        return username  # Return username if login was successful
    else:
        print(f"{Fore.RED}Incorrect password. Try again. Returning to main menu.")
        return None  # Return None if the password is incorrect
