# tasks.py


from datetime import datetime
from colorama import Fore,init
import  shortuuid
from google_sheets import save_data_to_sheet
from validators import *


CATEGORY_MAPPING = {"P": "personal", "B": "business"}
STATUS_MAPPING = {"P": "Pending", "IP": "In Progress", "C": "Complete"}

init(autoreset=True)


def add_task(username, users):
    """
    Add a new task for the user after validating inputs.

    Parameters:
        username (str): The username of the user.
        users (dict): A dictionary containing user data.

    Returns:
        None
    """
    # Validate inputs
    name = validate_name()
    if name is None:
        print(f"{Fore.LIGHTYELLOW_EX}Back to TaskMenu!")
        return

    due_date = validate_date()
    if due_date is None:
        print(f"{Fore.LIGHTYELLOW_EX}Back to TaskMenu!")
        return

    priority = validate_priority()
    if priority is None:
        return

    category = validate_category()
    if category is None:
        return

    description = validate_description()
    if description is None:
        return

    status = validate_status()
    if status is None:
        return

    # Create the task dictionary with a unique ID
    task = {
        "id": shortuuid.uuid()[:4],  # Generate a unique ID
        "name": name,
        "due_date": due_date,
        "priority": priority,
        "category": category,
        "description": description,
        "status": status,
    }

    # Add the task to the user's task list
    users[username]["tasks"].setdefault(category, []).append(task)

    # Save the updated users data to Google Sheets
    save_data_to_sheet(users)

    print(Fore.GREEN + "Task added successfully!")

def list_tasks(username, users):
    """
    List all tasks for the user.

    Parameters:
        username (str): The username of the user.
        users (dict): A dictionary containing user data.

    Returns:
        None
    """
    user_data = users.get(username, {})
    user_tasks = user_data.get("tasks", {})

    # Use um filtro para encontrar tarefas pessoais e de negócios
    personal_tasks = [
        task for task in user_tasks.get("personal", [])
        if task["category"] in ["p", "personal"]
    ]
    business_tasks = [
        task for task in user_tasks.get("business", [])
        if task["category"] in ["b", "business"]
    ]

    if not personal_tasks and not business_tasks:
        print(Fore.RED + "No tasks found for this user.")
        return

    # Display personal tasks
    if personal_tasks:
        print(Fore.MAGENTA + "-" * 50)
        print(f"{Fore.WHITE}{' ' * 15} Personal Tasks:")
        for task in personal_tasks:
            print_task_details(task)
    else:
        print("No Personal Tasks")

    # Display business tasks
    if business_tasks:
        print(Fore.MAGENTA + "-" * 50)
        print(f"{' ' * 15} Business Tasks:")
        for task in business_tasks:
            print_task_details(task)
    else:
        print("No Business Tasks")


def print_task_details(task):
    """
    Print details of a task.

    Parameters:
        task (dict): A dictionary representing a task.

    Returns:
        None
    """
    print(Fore.MAGENTA + "-" * 50)
    print(f"{Fore.GREEN}Task ID: {task['id']}")
    print(f"{Fore.GREEN}Name: {task['name']}")
    print(f"{Fore.GREEN}Due Date: {task['due_date']}")
    print(f"{Fore.GREEN}Priority: {task['priority']}")
    print(f"{Fore.GREEN}Description: {task['description']}")
    print(f"{Fore.GREEN}Status: {task['status']}")
    print(Fore.MAGENTA + "-" * 50)

def sort_tasks_menu(user_tasks):
    """
    Display sorting menu and sort tasks based on user input.

    Parameters:
        user_tasks (dict): Dictionary of tasks categorized by personal and business.

    Returns:
        None
    """
    all_tasks = user_tasks.get("personal", []) + user_tasks.get("business", [])
    if not all_tasks:
        print(f"{Fore.RED}No tasks available to sort.")
        return

    list_tasks(user_tasks)  # Presumindo que a função list_tasks existe

    while True:
        sort_criteria = (
            input(
                "Enter the sorting criteria (name, due_date, priority, status) or type 'quit' to exit: "
            )
            .strip()
            .lower()
        )
        if sort_criteria == "quit":
            return
        if sort_criteria not in ["name", "due_date", "priority", "status"]:
            print(
                f"{Fore.RED}Invalid sorting criteria. Please enter one of the following: name, due_date, priority, status."
            )
            continue

        if sort_criteria == "due_date":
            sorted_tasks = sort_by_due_date(all_tasks)
        elif sort_criteria == "priority":
            print("Sorted tasks priority: High / Medium / Low")
            sorted_tasks = sort_by_priority(all_tasks)
        elif sort_criteria == "status":
            print("Sorted tasks Status: In Progress / Pending / Complete")
            sorted_tasks = sort_by_status(all_tasks)
        else:
            sorted_tasks = sorted(
                all_tasks, key=lambda x: x.get(sort_criteria, "")
            )

        print_sorted_tasks(sorted_tasks)
        break


def print_sorted_tasks(sorted_tasks):
    """
    Print sorted tasks.

    Parameters:
        sorted_tasks (list): A list of tasks sorted based on a criteria.

    Returns:
        None
    """
    if sorted_tasks:
        print("Sorted Tasks:")
        for i, task in enumerate(sorted_tasks, start=1):
            task_id = f"{task['category']}{i}"
            print_task_details(task, task_id)
    else:
        print("No tasks to display.")


def sort_by_priority(tasks):
    """
    Sort tasks by their priority.

    Parameters:
        tasks (list): A list of tasks.

    Returns:
        list: Sorted list of tasks by priority.
    """
    priority_order = {"low": 3, "medium": 2, "high": 1}
    return sorted(
        tasks, key=lambda x: priority_order.get(x["priority"], float("inf"))
    )


def sort_by_due_date(tasks, reverse=False):
    """
    Sort tasks by their due date.

    Parameters:
        tasks (list): A list of tasks.

    Returns:
        list: Sorted list of tasks by due date.
    """
    return sorted(
        tasks,
        key=lambda x: datetime.strptime(x["due_date"], "%d-%m-%Y"),
        reverse=reverse,
    )


def sort_by_status(tasks):
    """
    Sort tasks by their status.

    Parameters:
        tasks (list): A list of tasks.

    Returns:
        list: Sorted list of tasks by status.
    """
    status_order = {"Pending": 1, "In Progress": 2, "Complete": 3}
    return sorted(
        tasks, key=lambda x: status_order.get(x["status"], float("inf"))
    )


def remove_task(username, users):
    """
    Remove a task for the user.

    Parameters:
        username (str): Username of the user.
        users (dict): A dictionary containing user data.

    Returns:
        None
    """
    user_tasks = users.get(username, {}).get("tasks", {})

    if not user_tasks:
        print(f"{Fore.RED}No tasks found for this user.")
        return

    list_tasks(username, users)  # List tasks before removal

    while True:
        task_id = input('Enter the Task ID to remove (or type "quit" to exit): ').strip()
        if task_id.lower() in ["quit", "exit"]:
            return

        task_found = False
        for _, tasks in user_tasks.items():  # Ignoring the category variable
            for i in range(len(tasks)):
                if tasks[i].get('id') == task_id:  # Use get() to avoid KeyError
                    task_found = True
                    removed_task = tasks.pop(i)  # Remove the task
                    print(f"{Fore.GREEN}Task '{removed_task['name']}' removed successfully.")
                    save_data_to_sheet(users)  # Save changes
                    break  # Break out of the inner loop
            if task_found:
                break  # Break out of the outer loop

        if not task_found:
            print(f"{Fore.RED}Invalid Task ID. Please try again.")

def update_task(username, users):
    """
    Update an existing task for the user.

    Parameters:
        username (str): Username of the user.
        users (dict): A dictionary containing user data.

    Returns:
        None
    """
    user_data = users.get(username, {})
    user_tasks = user_data.get("tasks", {})
    if not user_tasks:
        print(f"{Fore.RED}No tasks found for this user.")
        return

    while True:
        category_code = input("Enter the category to update (P for Personal, B for Business), or type 'quit' to exit: ").strip().upper()
        if category_code == "QUIT":
            return
        if category_code not in CATEGORY_MAPPING:
            print(f"{Fore.RED}Error: Invalid category. Please enter 'P' for Personal or 'B' for Business.")
            continue

        category = CATEGORY_MAPPING[category_code]
        tasks_in_category = user_tasks.get(category, [])

        if not tasks_in_category:
            print(f"{Fore.RED}{category} Tasks are empty.")
            continue

        list_tasks({category: tasks_in_category})  # Presumindo que a função list_tasks existe

        task_id = input(f"Enter the Task ID to update in category {category_code} (e.g., {category_code}1), or type 'quit' to exit: ").strip().upper()
        if task_id == "QUIT":
            return
        if not task_id.startswith(category_code) or len(task_id) < 2:
            print(f"{Fore.RED}Invalid Task ID format. Please ensure it matches the format (e.g., P1, B2).")
            continue

        try:
            task_index = int(task_id[1:]) - 1
            if task_index < 0 or task_index >= len(tasks_in_category):
                print(f"{Fore.RED}Task ID out of range. Please enter a valid Task ID.")
                continue
        except ValueError:
            print(f"{Fore.RED}Invalid Task ID format. Please ensure it ends with a number (e.g., P1, B2).")
            continue

        task = tasks_in_category[task_index]
        print("Current task details:")
        print_task_details(task, task_id)

        task["name"] = input("Enter new task name (leave blank to keep current): ") or task["name"]
        task["due_date"] = input("Enter new due date (leave blank to keep current): ") or task["due_date"]
        task["priority"] = input("Enter new priority (low, medium, high; leave blank to keep current): ").lower() or task["priority"]
        task["description"] = input("Enter new description (leave blank to keep current): ") or task["description"]
        task["status"] = input("Enter new status (Not Started, In Progress, Complete; leave blank to keep current): ").upper() or task["status"]

        # Salvar os dados atualizados de volta na planilha
        save_data_to_sheet(users)

        print(f"{Fore.GREEN}Task updated successfully.")
        break

def update_field_menu(task):
    """
    Update fields of a task.

    Parameters:
        task (dict): A dictionary representing a task.

    Returns:
        None
    """
    while True:
        print("Select field to update:")
        print("1. Name")
        print("2. Due Date")
        print("3. Priority")
        print("4. Description")
        print("5. Status")
        print("6. Back to main menu")

        field_choice = input("Enter your choice: ")

        if field_choice == "1":
            new_name = input("Enter the new name for the task: ")
            task["name"] = new_name
        elif field_choice == "2":
            new_due_date = input(
                "Enter the new due date for the task (YYYY-MM-DD): "
            )
            task["due_date"] = new_due_date
        elif field_choice == "3":
            new_priority = input(
                "Enter the new priority for the task (high/medium/low): "
            ).lower()
            if new_priority in ["high", "medium", "low"]:
                task["priority"] = new_priority
            else:
                print(
                    f"{Fore.RED}Invalid priority. Please enter 'high', 'medium', or 'low'."
                )
        elif field_choice == "4":
            new_description = input("Enter the new description for the task: ")
            task["description"] = new_description
        elif field_choice == "5":
            new_status = input(
                "Enter the new status for the task (P for Pending, IP for In Progress, C for Complete): "
            ).upper()
            if new_status in ["P", "IP", "C"]:
                task["status"] = new_status
            else:
                print(
                    f"{Fore.RED}Invalid status. Please enter 'P' for Pending, 'IP' for In Progress, or 'C' for Complete."
                )
        elif field_choice == "6":
            break  # Volta para o menu principal
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 6.")


def check_empty_list(tasks, message):
    """
    Checks if the tasks it really exist
    and in case not, can't have a speficic message; related to that task
    Parameters:
    tasks(list with the dict within the dict represent the task)
    message: Personalized message in case not find the tasks

    Return:
    True or False
    """
    if not tasks:
        print(message)
        return True
    return False



