# tasks.py

import json
import memcache
from datetime import datetime
from cache_utils import set_user_tasks
from colorama import Fore


CATEGORY_MAPPING = {"P": "personal", "B": "business"}
STATUS_MAPPING = {"P": "Pending", "IP": "In Progress", "C": "Complete"}


def list_tasks(user_tasks):
    """
    List all tasks for the user.

    Parameters:
        user_tasks (dict): A dictionary containing user tasks.

    Returns:
        None
    """
    all_tasks = [
        task
        for category_tasks in user_tasks.values()
        for task in category_tasks
    ]

    if not all_tasks:
        print("No tasks found for this user.")
        return

    personal_tasks = [task for task in all_tasks if task["category"] == "P"]
    business_tasks = [task for task in all_tasks if task["category"] == "B"]
    if personal_tasks:
        print(Fore.MAGENTA + "-" * 50)
        print(f"{Fore.WHITE}{ ' ' * 15} Personal Tasks:")
        for i, task in enumerate(personal_tasks, start=1):
            print_task_details(task, f"P{i}")
    else:
        print("No Personal Tasks")

    if business_tasks:
        print(f'{ " " * 15} Business Tasks:')
        for i, task in enumerate(business_tasks, start=1):
            print_task_details(task, f"B{i}")


def print_task_details(task, task_id):
    """
    Print details of a task.

    Parameters:
        task (dict): A dictionary representing a task.
        task_id (str): ID of the task.

    Returns:
        None
    """

    print(Fore.MAGENTA + "-" * 50)
    print(f"{Fore.GREEN}Task ID: {task_id}")
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

    list_tasks(user_tasks)

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
    Sort tasks by their status.

    Parameters:
        tasks (list): A list of tasks.

    Returns:
        list: Sorted list of tasks by status.
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


def remove_task(username, user_data):
    """
    Remove a task for the user.

    Parameters:
        username (str): Username of the user.
        user_data (dict): A dictionary containing user data.

    Returns:
        None
    """
    user_tasks = user_data.get("tasks", {})
    if not user_tasks:
        print("No tasks found for this user.")
        return

    list_tasks(user_tasks)

    while True:
        task_id = input(
            'Enter the Task ID to remove (e.g., P1, B2) or type "quit" to exit: '
        ).strip()
        if task_id.lower() in ["quit", "exit"]:
            return
        if not task_id or len(task_id) < 2:
            print("Please enter a valid Task ID.")
            continue

        category_code = task_id[0].upper()
        if category_code not in CATEGORY_MAPPING:
            print(
                'Invalid Task ID format. It should start with "P" or "B" followed by a number.'
            )
            continue

        category = CATEGORY_MAPPING[category_code]
        try:
            task_index = int(task_id[1:]) - 1
            if task_index < 0 or task_index >= len(
                user_tasks.get(category, [])
            ):
                raise ValueError(
                    "Task ID out of range. Please enter a valid Task ID."
                )
        except ValueError as e:
            print(f"Error: {e}")
            continue

        user_tasks[category].pop(task_index)

        # Atualizar o cache com os dados do usuário
        set_user_tasks(username, user_tasks)

        print("Task removed successfully.")
        break


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
        print("No tasks found for this user.")
        return

    while True:
        category_code = (
            input(
                "Enter the category to update (P for Personal, B for Business), or type 'quit' to exit: "
            )
            .strip()
            .upper()
        )
        if category_code == "QUIT":
            return
        if category_code not in CATEGORY_MAPPING:
            print(
                "Error: Invalid category. Please enter 'P' for Personal or 'B' for Business."
            )
            continue

        category = CATEGORY_MAPPING[category_code]
        tasks_in_category = user_tasks.get(category, [])

        if not tasks_in_category:
            print(f"{category} Tasks are empty.")
            continue

        list_tasks({category: tasks_in_category})

        task_id = (
            input(
                f"Enter the Task ID to update in category {category_code} (e.g., {category_code}1), or type 'quit' to exit: "
            )
            .strip()
            .upper()
        )
        if task_id == "QUIT":
            return
        if not task_id.startswith(category_code) or len(task_id) < 2:
            print(
                "Invalid Task ID format. Please ensure it matches the format (e.g., P1, B2)."
            )
            continue

        try:
            task_index = int(task_id[1:]) - 1
            if task_index < 0 or task_index >= len(tasks_in_category):
                print("Task ID out of range. Please enter a valid Task ID.")
                continue
        except ValueError:
            print(
                "Invalid Task ID format. Please ensure it ends with a number (e.g., P1, B2)."
            )
            continue

        task = tasks_in_category[task_index]
        print("Current task details:")
        print_task_details(task, task_id)

        task["name"] = input(
            "Enter new task name (leave blank to keep current): "
        )
        task["due_date"] = input(
            "Enter new due date (leave blank to keep current): "
        )
        task["priority"] = input(
            "Enter new priority (low, medium, high; leave blank to keep current): "
        ).lower()
        task["description"] = input(
            "Enter new description (leave blank to keep current): "
        )
        task["status"] = input(
            "Enter new status (Not Started, In Progress, Complete; leave blank to keep current): "
        ).upper()

        # Atualizar o arquivo JSON com os dados do usuário
        with open("users_data.json", "w") as file:
            json.dump(users, file, indent=4)

        print("Task updated successfully.")
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
                    "Invalid priority. Please enter 'high', 'medium', or 'low'."
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
                    "Invalid status. Please enter 'P' for Pending, 'IP' for In Progress, or 'C' for Complete."
                )
        elif field_choice == "6":
            break  # Volta para o menu principal
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


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
