# auth.py

import json

def load_user_data():
    try:
        with open('users_data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(users):
    with open('users_data.json', 'w') as file:
        json.dump(users, file, indent=4)

def login_user(users):
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in users and users[username]['password'] == password:
            print(f"Authentication successful! Welcome back, {username}")
            return username
        else:
            print("Invalid username or password. Please try again.")

def register_user(users):
    while True:
        try:
            username = input("Enter username: ").strip()
            if len(username) < 5:
                raise ValueError("Username must be at least 5 characters long.")
            
            password = input("Enter password: ").strip()
            if len(password) < 5:
                raise ValueError("Password must be at least 5 characters long.")
            
            if username in users:
                print("Username already exists. Please choose a different username.")
            else:
                users[username] = {'password': password, 'tasks': {'personal': [], 'business': []}}
                save_user_data(users)
                print(f"User {username} registered successfully!")
                return username, users
        except ValueError as ve:
            print(f"Error: {ve}")

