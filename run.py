import json
from datetime import datetime
# from validotor import * / criar um outro file
import os

CATEGORY_MAPPING = {'P': 'personal', 'B': 'business'}
STATUS_MAPPING = {'C': 'Complete', 'P': 'Pending', 'IP': 'In Progress'}

def add_task(username, user_data):
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
            user_data[username]['tasks']['personal'].append(task)
            print('Task successfully inserted into Personal category')
        elif category == 'B':
            user_data[username]['tasks']['business'].append(task)
            print('Task successfully inserted into Business category')    
        else:
            print('Invalid category')
            continue
        
        with open('users_data.json', 'w') as file:
            json.dump(user_data, file, indent=4)
        
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

def list_tasks(user_tasks, category_input):
    category = CATEGORY_MAPPING.get(category_input)
    mapped_category = category if category else 'Unknown'

    high_priority = []
    medium_priority = []
    low_priority = []

    if mapped_category not in user_tasks or not user_tasks[mapped_category]:
        print(f"{mapped_category.capitalize()} Tasks: None")
        return

    for i, task in enumerate(user_tasks[mapped_category]):
        if task['priority'] == 'high':
            high_priority.append((i + 1, task))
        elif task['priority'] == 'medium':
            medium_priority.append((i + 1, task))
        elif task['priority'] == 'low':
            low_priority.append((i + 1, task))

    print(f"{mapped_category.capitalize()} Tasks:")

    if not high_priority:
        print("High Priority Tasks are empty at the moment")
    else:
        print("High Priority:")
        for task_id, task in high_priority:
            print_task_details(task, task_id)

    if not medium_priority:
        print("Medium Priority Tasks are empty at the moment")
    else:
        print("Medium Priority:")
        for task_id, task in medium_priority:
            print_task_details(task, task_id)

    if not low_priority:
        print("Low Priority Tasks are empty at the moment")
    else:
        print("Low Priority:")
        for task_id, task in low_priority:
            print_task_details(task, task_id)

    while True:
        print("Sort Options:")
        print("1. By Due Date (closest first)")
        print("2. By Due Date (farthest first)")
        print("3. By Status")
        print("4. Back to Main Menu")

        try:
            sort_option = int(input("Enter your choice: "))
            if sort_option not in [1, 2, 3, 4]:
                raise ValueError("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if sort_option == 1:
            sorted_tasks = sort_by_due_date(user_tasks[mapped_category], reverse=False)
            print("Tasks closest first:")
            for i, task in enumerate(sorted_tasks):
                print_task_details(task, i + 1)
        elif sort_option == 2:
            sorted_tasks = sort_by_due_date(user_tasks[mapped_category], reverse=True)
            print("Tasks farthest first:")
            for i, task in enumerate(sorted_tasks):
                print_task_details(task, i + 1)
        elif sort_option == 3:
            sorted_tasks = sort_by_status(user_tasks[mapped_category])
            print('Tasks by Status order: "Pending"; "In Progress"; "Complete"')
            for i, task in enumerate(sorted_tasks):
                print_task_details(task, i + 1)
        elif sort_option == 4:
            print("Returning to the Main Menu.")
            break

def sort_by_due_date(tasks, reverse=False):
    return sorted(tasks, key=lambda x: datetime.strptime(x['due_date'], "%d-%m-%Y"), reverse=reverse)


def sort_by_status(tasks):
    status_order = {"Pending": 1, "In Progress": 2, "Complete": 3}
    return sorted(tasks, key=lambda x: status_order.get(x['status'], float('inf')))

def print_task_details(task, task_id):
    category_full_name = CATEGORY_MAPPING.get(task['category'], 'Unknown')
    print(f"Task ID: {task_id}")
    print(f"Name: {task['name']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Priority: {task['priority']}")
    print(f"Category: {category_full_name}")
    print(f"Description: {task['description']}")
    print(f"Status: {task['status']}")
    print("-----------")

def remove_task(user_data, username):
    user_tasks = user_data.get(username, {}).get('tasks', {})
    if not user_tasks:
        print('No tasks found for this user.')
        return

    view_all_tasks(user_tasks)
    
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
            if task_index < 0 or task_index >= len(user_tasks[category]):
                raise ValueError('Task ID out of range. Please enter a valid Task ID.')
        except ValueError as e:
            print(f'Error: {e}')
            continue
        
        user_tasks[category].pop(task_index)
        
        with open('users_data.json', 'w') as file:
            json.dump(user_data, file, indent=4)
        
        print('Task removed successfully.')
        break


def update_task(username, user_data):
    user_tasks = user_data.get(username, {}).get('tasks', {})
    if not user_tasks:
        print('No tasks found for this user.')
        return

    view_all_tasks(user_tasks)

    while True:
        try:
            task_id = input('Enter the Task ID to update (or type "quit" to exit): ')
            if task_id.lower() in ['quit', 'exit']:
                return
            if not task_id.strip():
                raise ValueError('Please, enter the Task ID, (or type "quit" to exit) field can\'t be empty')
            task_id = int(task_id)

            while True:
                try:
                    category = input('Enter the category of the task to update (P - Personal, B - Business) (or type "quit" to exit): ').upper()
                    if category.lower() in ['quit', 'exit']:
                        return
                    if not category.strip():
                        raise ValueError('Please, enter the correct category: (P - Personal, B - Business), (or type "quit" to exit) field can\'t be empty')
                    mapped_category = CATEGORY_MAPPING.get(category)

                    if mapped_category not in user_tasks:
                        raise ValueError('Invalid category')

                    tasks = user_tasks[mapped_category]
                    if task_id < 1 or task_id > len(tasks):
                        raise ValueError('Invalid Task ID in this Category')

                    task_index = task_id - 1
                    task = tasks[task_index]
                    break  # Break do loop de categoria se tudo estiver certo
                except ValueError as e:
                    print(f'Error: {e}')

            while True:
                print_task_details(task, task_id)
                print('Select the field to update:')
                print('1. Name')
                print('2. Due Date')
                print('3. Priority')
                print('4. Category')
                print('5. Description')
                print('6. Status')
                print('7. Back to Main Menu')

                try:
                    field_choice = input('Enter your choice: ')
                    if not field_choice.strip():
                        print('Please enter a valid choice.')
                        continue
                    field_choice = int(field_choice)
                    if field_choice not in range(1, 8):
                        print('Invalid choice. Please enter a number between 1 and 7.')
                        continue
                except ValueError:
                    print('Invalid input. Please enter a valid number.')
                    continue  # Continuar perguntando no loop interno até obter uma entrada válida

                if field_choice == 1:
                    new_name = validate_name()
                    if new_name:
                        task['name'] = new_name
                        print('Task name updated successfully')
                elif field_choice == 2:
                    new_due_date = validate_date()
                    if new_due_date:
                        task['due_date'] = new_due_date
                        print('Task Due Date updated successfully')
                elif field_choice == 3:
                    new_priority = validate_priority()
                    if new_priority:
                        task['priority'] = new_priority
                        print('Task Priority updated successfully')
                elif field_choice == 4:
                    new_category = validate_category()
                    if new_category:
                        new_mapped_category = CATEGORY_MAPPING.get(new_category)
                        if new_mapped_category and new_mapped_category != mapped_category:
                            tasks.pop(task_index)
                            user_tasks[new_mapped_category].append(task)
                            # Atualize a referência da lista de tarefas
                            user_tasks[mapped_category] = tasks
                            mapped_category = new_mapped_category
                            print('Task Category updated successfully')
                            # Salvar as alterações no arquivo JSON após a atualização da categoria
                            with open('users_data.json', 'w') as file:
                                json.dump(user_data, file, indent=4)
                            break  # Sair do loop para permitir a atualização do mapeamento da categoria
                elif field_choice == 5:
                    new_description = validate_description()
                    if new_description:
                        task['description'] = new_description
                        print('Task Description updated successfully')
                elif field_choice == 6:
                    new_status = validate_status()
                    if new_status:
                        task['status'] = STATUS_MAPPING[new_status]
                        print('Task Status updated successfully')
                elif field_choice == 7:
                    return

                # Salvar as alterações no arquivo JSON
                with open('users_data.json', 'w') as file:
                    json.dump(user_data, file, indent=4)

                break  # Sair do loop interno após a atualização de um campo

        except ValueError as e:
            print(f'Error: {e}')

def load_user_data():
    if os.path.exists('users_data.json'):
        with open('users_data.json', 'r') as file:
            return json.load(file)
    return {}

def register_user(users):
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in users:
            print("Username already exists. Please choose a different username.")
        else:
            users[username] = {'password': password, 'tasks': {'personal': [], 'business': []}}
            print(f"User {username} registered successfully!")
            return username, users

def login_user(users):
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in users and users[username]['password'] == password:
            print(f"Authentication successful! Welcome back, {username}")
            return username
        else:
            print("Invalid username or password. Please try again.")

def check_empty_list(task_list, message):
    if not task_list:
        print(message)
        return True
    return False

def view_all_tasks(user_tasks):
    if not user_tasks.get('personal') and not user_tasks.get('business'):
        print('No tasks found.')
        return
    
    if user_tasks.get('personal'):
        print('Personal Tasks:')
        for idx, task in enumerate(user_tasks['personal']):
            print(f'Task ID: P{idx + 1}')
            print(f'Name: {task["name"]}')
            print(f'Due Date: {task["due_date"]}')
            print(f'Priority: {task["priority"]}')
            print(f'Category: Personal')
            print(f'Description: {task["description"]}')
            print(f'Status: {task["status"]}')
            print('-----------')
    
    if user_tasks.get('business'):
        print('Business Tasks:')
        for idx, task in enumerate(user_tasks['business']):
            print(f'Task ID: B{idx + 1}')
            print(f'Name: {task["name"]}')
            print(f'Due Date: {task["due_date"]}')
            print(f'Priority: {task["priority"]}')
            print(f'Category: Business')
            print(f'Description: {task["description"]}')
            print(f'Status: {task["status"]}')
            print('-----------')
            
def task_menu(username, users):
    user_data = users[username]
    user_tasks = user_data['tasks']
    
    while True:
        print("1. Add task")
        print("2. List tasks by Category : Personal/Business")
        print("3. Update task status")
        print("4. Remove task")
        print("5. Edit task")
        print("6. View all tasks")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_task(username, users)
        elif choice == '2':
            while True:
                try:
                    category_input = input("Enter category (P for Personal, B for Business): ").upper()
                    if category_input not in ['P', 'B']:
                        raise ValueError("Invalid category. Please enter 'P' for Personal or 'B' for Business.")
                    category = CATEGORY_MAPPING.get(category_input)
                    if not user_tasks.get(category):
                        print(f"{category.capitalize()} Tasks are empty.")
                    else:
                        list_tasks(user_tasks, category_input)
                    break  # Exit the loop if no errors occur
                except ValueError as ve:
                    print(f"Error: {ve}")
        elif choice == '3':
            if not check_empty_list(user_tasks['personal'] + user_tasks['business'], 'No tasks available to update.'):
                update_task(username, users)
        elif choice == '4':
            if not check_empty_list(user_tasks['personal'] + user_tasks['business'],'No tasks available to delete.'):
                remove_task(users, username)
        elif choice == '5':
            if not check_empty_list(user_tasks['personal'] + user_tasks['business'],'No tasks available to edit.'):
                update_task(username, users)
        elif choice == '6':
            if not check_empty_list(user_tasks['personal'] + user_tasks['business'], 'No tasks to view'):
                view_all_tasks(user_tasks)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

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
            with open('users_data.json', 'w') as file:
                json.dump(users, file, indent=4)
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.") 
            
print('Welcome to your TaskManager')
main()
