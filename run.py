from auth import login, register_user
from google_sheets import load_data_from_sheet, save_data_to_sheet
from tasks import list_tasks, remove_task, update_task,  sort_tasks_menu
from colorama import Fore, init
from tasks import add_task
from art import text2art

# Initialize colorama for colored console output
init(autoreset=True)

# Define mappings for task categories and statuses
CATEGORY_MAPPING = {"P": "personal", "B": "business"}
STATUS_MAPPING = {"C": "Complete", "P": "Pending", "IP": "In Progress"}

def main():
    """
    Main function to run the Task Manager application.
    This function loads user data from Google Sheets, displays the main menu for the user 
    to either register or log in, and navigates them to the task menu upon successful login or registration.
    """
    # Load users data from Google Sheets
    users_data = load_data_from_sheet()

    # Main loop to handle user input and application flow
    while True:
        # Display the Task Manager title using ASCII art
        print(Fore.CYAN + text2art(" Task Manager "))
        
        # Display menu options for Register and Login
        print(Fore.YELLOW + "1. Register - You can easily sign up now to start organizing your tasks")
        print(Fore.YELLOW + "2. Login - If you already have an account with us")
        
        # Prompt the user to enter their choice
        choice = input(Fore.CYAN + "Enter your choice: ")

        # Handle user registration
        if choice == "1":
            username = register_user(users_data)  # Register the user and return their username
            if username:
                # If registration is successful, navigate to the task menu
                task_menu(username, users_data)
        # Handle user login
        elif choice == "2":
            username = login(users_data)  # Attempt login and return the username if successful
            if username:
                # If login is successful, navigate to the task menu
                task_menu(username, users_data)
        
        # Handle invalid menu choice
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.")


def task_menu(username, users):
    """
    Display the task menu for the logged-in user.

    Args:
        username (str): The username of the logged-in user.
        users (dict): The dictionary containing user data.

    Returns:
        None
    """
    

    

    while True:
        print(Fore.CYAN + text2art("Task Menu"))
        print(Fore.YELLOW + "1. Add Task")
        print(Fore.YELLOW + "2. View All Tasks ")
        print(Fore.YELLOW + "3. Edit Task")
        print(Fore.YELLOW + "4. Remove Task")
        print(Fore.YELLOW + "5. Sort Tasks")
        print(Fore.YELLOW + "6. Logout")

        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == "1":
            add_task(username, users)
        elif choice == "2":
            list_tasks(username, users)
            
        elif choice == "3":
            update_task(username, users)
        elif choice == "4":
            remove_task(username, users)
            
        #elif choice == "5":
        #    sort_tasks_menu(user_tasks)
        elif choice == "6":
            print(Fore.GREEN + "Logging out.")
            break
        else:
            print(
                Fore.RED
                + "Invalid choice. Please enter a number between 1 and 6."
            )


if __name__ == "__main__":
    users = load_data_from_sheet()
    try:
        main()
        save_data_to_sheet(users)
    except Exception as e:
        pass
    finally:
        # Save data if an exception occurs
        pass
