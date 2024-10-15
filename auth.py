from colorama import Fore, init
import bcrypt
import pwinput
from google_sheets import  save_data_to_sheet
from validators import validate_username, validate_login_password, validate_password


# Initialize colorama for text formatting
init(autoreset=True)

def register_user(users_data):
    """
    Register a new user with a unique username and hashed password.

    Args:
        users_data (dict): Dictionary containing all user data.

    Returns:
        str: The registered username.
    """
    username = validate_username()

    # Ensure the username is unique
    while username in users_data:
        print("Username already exists.")
        username = validate_username()

    # Validate and hash the user's password
    password = validate_password()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    confirm_password = pwinput.pwinput("Confirm your password: ")
    if confirm_password == password:
        # Store user data with tasks categorized as 'personal' and 'business'
        users_data[username] = {
            "password": hashed_password,
            "tasks": {
                "personal": [],
                "business": []
            }
        }

        print(f"{Fore.GREEN}User registered successfully.")
        save_data_to_sheet(users_data)
        return username
    else:
        print(f"{Fore.RED} Passwords not match. Returning to Main Menu")

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
        print(f"{Fore.RED}Username not found. Returning to main menu.")
        return None  # Return None if username doesn't exist

    # Verify the input password matches the stored hashed password
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8')):
        print(f"{Fore.GREEN}Login successful! Welcome back {username}")
        return username  # Return username if login was successful
    else:
        print(f"{Fore.RED}Incorrect password. Try again. Returning to main menu.")
        return None  # Return None if the password is incorrect
