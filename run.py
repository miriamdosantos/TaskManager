

import os
import json
import memcache
from datetime import datetime

# Configure Memcached
memcached_servers = os.getenv('MEMCACHIER_SERVERS', 'localhost:11211')
memcached_username = os.getenv('MEMCACHIER_USERNAME', '')
memcached_password = os.getenv('MEMCACHIER_PASSWORD', '')

# Build the connection string with authentication
if memcached_username and memcached_password:
    memcached_servers_with_auth = f'{memcached_username}:{memcached_password}@{memcached_servers}'
else:
    memcached_servers_with_auth = memcached_servers

# Connect to Memcached
mc = memcache.Client([memcached_servers_with_auth], debug=0)

CATEGORY_MAPPING = {'P': 'personal', 'B': 'business'}
STATUS_MAPPING = {'C': 'Complete', 'P': 'Pending', 'IP': 'In Progress'}

def add_task(username, users):
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
        
        # Salvar os dados após adicionar a nova tarefa
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


def validate_name():
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
    while True:
        try:
            description = input('Enter the description: (maximum 50 characters, press Enter to skip) (or type "quit" to exit): ')
            if description.lower() in ['quit', 'exit']:
                return None
            if len(description) > 50 :
                raise ValueError('Exceeded the input. Maximum characters allowed: 50')
            if not description.strip():
                return "" 
            return description
        except ValueError as e:
            print(f'Error: {e}')

def validate_status():
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

def get_user_tasks(username):
    user_tasks = mc.get(username)
    if not user_tasks:
        return {'personal': [], 'business': []}
    return json.loads(user_tasks)

def set_user_tasks(username, tasks):
    mc.set(username, json.dumps(tasks))

def list_tasks(user_tasks):
    all_tasks = [task for category_tasks in user_tasks.values() for task in category_tasks]

    if not all_tasks:
        print("No tasks found for this user.")
        return

    personal_tasks = [task for task in all_tasks if task['category'] == 'P']
    business_tasks = [task for task in all_tasks if task['category'] == 'B']

    if personal_tasks:
        print("Personal Tasks:")
        for i, task in enumerate(personal_tasks, start=1):
            print_task_details(task, f"P{i}")
    else:
        print("No Personal Tasks")

    if business_tasks:
        print("Business Tasks:")
        for i, task in enumerate(business_tasks, start=1):
            print_task_details(task, f"B{i}")
    else:
        print("No Business Tasks")

def print_task_details(task, task_id):
    print(f"Task ID: {task_id}")
    print(f"Name: {task['name']}")
    print(f"Due Date : {task['due_date']}")
    print(f"Priority: {task['priority']}")
    print(f"Category: {task['category'].capitalize()}")
    print(f"Description: {task['description']}")
    print(f"Status: {task['status']}")
    print("-----------")


def sort_tasks_menu(user_tasks):
    all_tasks = [task for category_tasks in user_tasks.values() for task in category_tasks]

    if not all_tasks:
        print("No tasks found for this user.")
        return

    list_tasks(user_tasks)

    while True:
        sort_criteria = input("Enter the sorting criteria (name, due_date, priority, status) or type 'quit' to exit: ").strip().lower()
        if sort_criteria == 'quit':
            return
        if sort_criteria not in ['name', 'due_date', 'priority', 'status']:
            print('Invalid sorting criteria. Please enter one of the following: name, due_date, priority, status.')
            continue

        sorted_tasks = sorted(all_tasks, key=lambda x: x.get(sort_criteria, ''))
        print_sorted_tasks(sorted_tasks)
        break

def print_sorted_tasks(sorted_tasks):
    if sorted_tasks:
        print("Sorted Tasks:")
        for i, task in enumerate(sorted_tasks, start=1):
            task_id = f"{task['category']}{i}"
            print_task_details(task, task_id)
    else:
        print("No tasks to display.")

def sort_by_due_date(tasks, reverse=False):
    return sorted(tasks, key=lambda x: datetime.strptime(x['due_date'], "%d-%m-%Y"), reverse=reverse)

def sort_by_status(tasks):
    status_order = {"Pending": 1, "In Progress": 2, "Complete": 3}
    return sorted(tasks, key=lambda x: status_order.get(x['status'], float('inf')))

def remove_task(username, user_data):  # Adicionando 'username' como parâmetro
    user_tasks = user_data.get('tasks', {})
    if not user_tasks:
        print('No tasks found for this user.')
        return

    list_tasks(user_tasks)

    while True:
        task_id = input('Enter the Task ID to remove (e.g., P1, B2) or type "quit" to exit: ').strip()
        if task_id.lower() in ['quit', 'exit']:
            return
        if not task_id or len(task_id) < 2:
            print('Please enter a valid Task ID.')
            continue

        category_code = task_id[0].upper()
        if category_code not in CATEGORY_MAPPING:
            print('Invalid Task ID format. It should start with "P" or "B" followed by a number.')
            continue

        category = CATEGORY_MAPPING[category_code]
        try:
            task_index = int(task_id[1:]) - 1
            if task_index < 0 or task_index >= len(user_tasks.get(category, [])):
                raise ValueError('Task ID out of range. Please enter a valid Task ID.')
        except ValueError as e:
            print(f'Error: {e}')
            continue

        user_tasks[category].pop(task_index)

        # Atualizar o cache com os dados do usuário
        set_user_tasks(username, user_tasks)

        print('Task removed successfully.')
        break


def update_task(username, users):  # Adicionar o argumento 'username'
    user_data = users.get(username, {})  # Obter os dados do usuário com base no nome de usuário
    user_tasks = user_data.get('tasks', {})  # Obter as tarefas do usuário dos dados do usuário
    if not user_tasks:
        print('No tasks found for this user.')
        return

    while True:
        category_code = input("Enter the category to update (P for Personal, B for Business), or type 'quit' to exit: ").strip().upper()
        if category_code == 'QUIT':
            return
        if category_code not in CATEGORY_MAPPING:
            print("Error: Invalid category. Please enter 'P' for Personal or 'B' for Business.")
            continue

        category = CATEGORY_MAPPING[category_code]
        tasks_in_category = user_tasks.get(category, [])

        if not tasks_in_category:
            print(f"{category} Tasks are empty.")
            continue

        list_tasks({category: tasks_in_category})

        task_id = input(f"Enter the Task ID to update in category {category_code} (e.g., {category_code}1), or type 'quit' to exit: ").strip().upper()
        if task_id == 'QUIT':
            return
        if not task_id.startswith(category_code) or len(task_id) < 2:
            print('Invalid Task ID format. Please ensure it matches the format (e.g., P1, B2).')
            continue

        try:
            task_index = int(task_id[1:]) - 1
            if task_index < 0 or task_index >= len(tasks_in_category):
                print('Task ID out of range. Please enter a valid Task ID.')
                continue
        except ValueError:
            print('Invalid Task ID format. Please ensure it ends with a number (e.g., P1, B2).')
            continue

        task = tasks_in_category[task_index]
        print("Current task details:")
        print_task_details(task, task_id)

        task['name'] = input('Enter new task name (leave blank to keep current): ')
        task['due_date'] = input('Enter new due date (leave blank to keep current): ')
        task['priority'] = input('Enter new priority (low, medium, high; leave blank to keep current): ').lower()
        task['description'] = input('Enter new description (leave blank to keep current): ')
        task['status'] = input('Enter new status (Not Started, In Progress, Complete; leave blank to keep current): ').upper()

        # Atualizar o arquivo JSON com os dados do usuário
        with open('users_data.json', 'w') as file:
            json.dump(users, file, indent=4)

        print('Task updated successfully.')
        break

def update_field_menu(task):
    while True:
        print("Select field to update:")
        print("1. Name")
        print("2. Due Date")
        print("3. Priority")
        print("4. Description")
        print("5. Status")
        print("6. Back to main menu")

        field_choice = input("Enter your choice: ")

        if field_choice == '1':
            new_name = input("Enter the new name for the task: ")
            task['name'] = new_name
        elif field_choice == '2':
            new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
            task['due_date'] = new_due_date
        elif field_choice == '3':
            new_priority = input("Enter the new priority for the task (high/medium/low): ").lower()
            if new_priority in ['high', 'medium', 'low']:
                task['priority'] = new_priority
            else:
                print("Invalid priority. Please enter 'high', 'medium', or 'low'.")
        elif field_choice == '4':
            new_description = input("Enter the new description for the task: ")
            task['description'] = new_description
        elif field_choice == '5':
            new_status = input("Enter the new status for the task (P for Pending, IP for In Progress, C for Complete): ").upper()
            if new_status in ['P', 'IP', 'C']:
                task['status'] = new_status
            else:
                print("Invalid status. Please enter 'P' for Pending, 'IP' for In Progress, or 'C' for Complete.")
        elif field_choice == '6':
            break  # Volta para o menu principal
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


def save_data(username, users):
    # Atualizar o cache com os dados do usuário
    user_tasks = users.get(username, {}).get('tasks', {})
    set_user_tasks(username, user_tasks)

    # Escrever os dados em um arquivo JSON
    with open('users_data.json', 'w') as file:
        json.dump(users, file, indent=4)
    # Escrever os dados em um arquivo JSON
    with open('users_data.json', 'w') as file:
        json.dump(users, file, indent=4)

def check_empty_list(tasks, message):
    if not tasks:
        print(message)
        return True
    return False

def load_user_data():
    try:
        with open('users_data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
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
                print(f"User {username} registered successfully!")
                return username, users
        except ValueError as ve:
            print(f"Error: {ve}")


def main():
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
    # Aqui não precisamos chamar save_data(users) porque já foi chamado dentro do bloco try
    pass