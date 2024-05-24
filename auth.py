# auth.py

import json
from colorama import Fore, Style, init

# Initialize colorama
init()
"""
    Load user data from the JSON file.

    Returns:
        dict: A dictionary containing user data.
    """


def load_user_data():
    try:
        with open("users_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_user_data(users):
    """
    Save user data to the JSON file.

    Parameters:
        users (dict): A dictionary containing user data.

    Returns:
        None
    """
    with open("users_data.json", "w") as file:
        json.dump(users, file, indent=4)


def login_user(users):
    """
    Login user.

    Parameters:
        users (dict): A dictionary containing user data.

    Returns:
        str: Username of the logged-in user.
    """
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in users and users[username]["password"] == password:
            print(
                f"{Fore.GREEN}Authentication successful! Welcome back, {username}{Style.RESET_ALL}"
            )
            return username
        else:
            print(
                f"{Fore.RED}Invalid username or password. Please try again.{Style.RESET_ALL}"
            )


def register_user(users):
    """
    Register a new user.

    Parameters:
        users (dict): A dictionary containing user data.

    Returns:
        tuple: Username and updated user data.
    """
    while True:
        try:
            username = input(
                'Enter username or type "quit" if you would like to not register anymore: '
            ).strip()
            if username.lower() == "quit":
                return None, users
            if len(username) < 5:
                raise ValueError("Username must be at least 5 characters long.")

            password = input(
                'Enter password or type "quit" if you would like to not register anymore: '
            ).strip()
            if password.lower() == "quit":
                return None, users
            if len(password) < 5:
                raise ValueError("Password must be at least 5 characters long.")

            if username in users:
                print(
                    f"{Fore.RED}Username already exists. Please choose a different username.{Style.RESET_ALL}"
                )
            else:
                users[username] = {
                    "password": password,
                    "tasks": {"personal": [], "business": []},
                }
                save_user_data(users)
                print(
                    f"{Fore.GREEN}User {username} registered successfully!{Style.RESET_ALL}"
                )
                return username, users
        except ValueError as ve:
            print(f"{Fore.RED}Error: {ve}{Style.RESET_ALL}")
