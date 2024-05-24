

# run.py

import json
from auth import *
from tasks import  list_tasks, remove_task, update_task, sort_tasks_menu
from validators import validate_name, validate_date, validate_priority, validate_category, validate_description, validate_status
import os
from cache_utils import save_data
import memcache
from tasks import  remove_task, list_tasks, update_task, sort_tasks_menu
from auth import load_user_data, save_user_data, login_user, register_user

CATEGORY_MAPPING = {'P': 'personal', 'B': 'business'}
STATUS_MAPPING = {'C': 'Complete', 'P': 'Pending', 'IP': 'In Progress'}

def add_task(username, users):
    """
    Add a new task for the specified user.

    Args:
        username (str): The username of the user.
        users (dict): The dictionary containing user data.

    Returns:
        None
    """
    while True:
        name = validate_name()
        if name is None:
            break
        
        due_date = validate_date()
        if due_date is None:
            break
        
        priority = validate_priority()
        if priority is None:
            break

        category = validate_category()
        if category is None:
            break
        
        description = validate_description()
        if description is None:
            break
        
        status_abbreviation = validate_status()
        if status_abbreviation is None:
            break
        
        status = STATUS_MAPPING.get(status_abbreviation, 'Unknown')
        task = {
            'name': name,
            'due_date': due_date,
            'priority': priority,
            'category': category,
            'description': description,
            'status': status,
        }

        if category == 'P':
            user_tasks = users[username]['tasks']
            user_tasks['personal'].append(task)
            print('Task successfully inserted into Personal category')
        elif category == 'B':
            user_tasks = users[username]['tasks']
            user_tasks['business'].append(task)
            print('Task successfully inserted into Business category')    
        else:
            print('Invalid category')
            continue
        
        # Save data after adding the new task
        save_data(username, users)
        
        while True:
            try:
                option = input('Would you like to add more tasks? (Y/N)').upper()
                if option not in ['Y', 'N']:
                    raise ValueError('Invalid input. Please answer: Y or N')
                elif option == 'Y':
                    break
                elif option == 'N':
                    return
            except ValueError as e:
                print(f'Error: {e}')




# Main function for running the Task Manager
def main():
    """
    Main function for running the Task Manager application.

    Returns:
        None
    """
    users = load_user_data()
    
    while True:
        print("1. Register - You can easily sign up now to start organizing your tasks")
        print("2. Login - If you already have an account with us")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username, users = register_user(users)
            task_menu(username, users)
        elif choice == '2':
            username = login_user(users)
            if username:
                task_menu(username, users)
        elif choice == '3':
            print("Quitting the program.")
            save_data(users)
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def task_menu(username, users):
    """
    Display the task menu for the logged-in user.

    Args:
        username (str): The username of the logged-in user.
        users (dict): The dictionary containing user data.

    Returns:
        None
    """
    user_data = users.get(username, {})
    if not user_data:
        print('User not found.')
        return

    user_tasks = user_data.get('tasks', {})
    if not user_tasks:
        print('No tasks found for this user.')
        return

    while True:
        print("Task Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Edit Task")
        print("4. View All Tasks")
        print("5. Sort Tasks")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_task(username, users)
        elif choice == '2':
            remove_task(username, user_data)  # Passando 'username' como primeiro argumento

        elif choice == '3':
            update_task(username, users)
        elif choice == '4':
            list_tasks(user_tasks)
        elif choice == '5':
            sort_tasks_menu(user_tasks)
        elif choice == '6':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
users = load_user_data()
               
try:
    main()
    save_data(users)
except Exception as e:
    pass
finally:
    # Save data if an exception occurs
    pass