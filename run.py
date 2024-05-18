import json #import json to transfor the data in JSON format, and can manipulate it
from datetime import datetime
import os


from datetime import datetime

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
        
        status = validate_status()
        if status is None:
            break
        
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
            continue  # Volta ao início do loop externo para solicitar uma nova entrada
        
        try: 
            option = input('Would you like to add more tasks? (Y/N)').upper()
            if option not in ['Y', 'N']:
                raise ValueError('Invalid input. Please answer: Y or N ')
        except ValueError as e:
             print(f'Error: {e}')
        
        if option == 'N':
            break

def validate_name():
    while True:
        try:
            name = input('Enter the task name (or type "quit" to exit): ')
            if name.lower() in ['quit', 'exit']:
                return None
            if not name.isalpha():
                raise ValueError("Invalid name. Name should only contain alphabetic characters.")
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
            return due_date.strftime("%d-%m-%Y")  # Retorna a data formatada
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
            description = input('Enter the description: (maximum 20 characters, press Enter to skip) (or type "quit" to exit): ')
            if description.lower() in ['quit', 'exit']:
                return None
            if len(description) > 20:
                raise ValueError('Exceeded the input. Maximum characters allowed: 20')
            if not description.strip():
                return None  # Retorna None se o usuário não fornecer uma descrição
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








         


        


def list_tasks(user_tasks, category):
    # Crie listas vazias para cada prioridade
    high_priority = []
    medium_priority = []
    low_priority = []
    
    tasks = user_tasks[category]
    # Separe as tarefas por prioridade dentro da categoria especificada
    # Separe as tarefas por prioridade
    for task in tasks:
        if task['priority'] == 'high':
            high_priority.append(task)
        elif task['priority'] == 'medium':
            medium_priority.append(task)
        elif task['priority'] == 'low':
            low_priority.append(task)
                
    # Imprima as tarefas separadas por prioridade
    print(f"{category.capitalize()} Tasks:")
    print("High Priority:")
    print_task_details(high_priority)
    print("Medium Priority:")
    print_task_details(medium_priority)
    print("Low Priority:")
    print_task_details(low_priority)

    # Opções de ordenação
    while True:
        print("Sort Options:")
        print("1. By Due Date (closest first)")
        print("2. By Due Date (farthest first)")
        print("3. By Status")
        print("4. Back to Main Menu")
        
        # Entrada do usuário
        try:
            sort_option = int(input("Enter your choice: "))
            if sort_option not in [1, 2, 3, 4]:
                raise ValueError("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        
        # Processamento da escolha do usuário
        if sort_option == 1:
            print_task_details(sort_by_due_date(user_tasks, category))
        elif sort_option == 2:
            print_task_details(sort_by_due_date(user_tasks, category, reverse=True))
        elif sort_option == 3:
            print_task_details(sort_by_status(user_tasks[category]))
        elif sort_option == 4:
            print("Returning to the Main Menu.")
            break  # Volta para o menu principal


def sort_by_due_date(user_tasks, category, reverse=False):
    # Lista para armazenar as tarefas ordenadas
    tasks_sorted = []

    tasks = user_tasks[category]  # Seleciona as tarefas na categoria especificada
    
    # Ordena as tarefas com base na data de vencimento
    tasks_sorted = sorted(tasks, key=lambda x: x['due_date'], reverse=reverse)

    return tasks_sorted



def view_all_tasks(user_tasks):
    print("All Tasks:")
    print("-----------")
    for i, task in enumerate(user_tasks['personal']):
        print(f"{i + 1}. {task['description']} - {task['status']}")
    print("Business Tasks:")
    for i, task in enumerate(user_tasks['business']):
        print(f"{i + 1}. {task['description']} - {task['status']}")
    


def print_task_details(task):
    # Função para imprimir os detalhes de uma tarefa
    print(f"Name: {task['name']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Priority: {task['priority']}")
    print(f"Status: {task['status']}")
    print(f"Description: {task['description']}")
    print()
    



def sort_by_status(user_task):
    tasks = user_task
    # Ordena as tarefas com base no status, utilizando uma função lambda
    sorted_tasks = sorted(tasks, key=lambda x: x['status'], reverse=True)
    return sorted_tasks


        
        



def update_status_task(user_task):
    tasks = user_task['tasks']
    while True:
        category = input("Enter the category (P for Personal, B for Business): ").upper()
        list_tasks(user_task, category)

        id = int(input("Enter the ID of the task to update the status: "))
        
        found_task = False
        for p, v in enumerate(tasks[category]):
            if id == p:
                v['status'] = input('Enter the new task status ("complete", "in progress", "pending"): ').lower()
                print("Task successfully updated")
                found_task = True
                break

        if not found_task:
            print('Invalid ID option. Please enter a valid ID.')
            continue  # Volta para o início do loop externo para solicitar um novo ID

        while True:
            update_another = input("Would you like to update another task? (Y/N): ").upper()
            if update_another in ('Y', 'N'):
                break
            else:
                print('Invalid input. Please enter Y or N.')
        
        if update_another == 'N':
            break  # Sai do loop externo se o usuário não quiser atualizar mais tarefas

def remove_task(user_task):
    tasks = user_task['tasks']
    while True:
        category = input("Enter the category (P for Personal, B for Business): ").upper()
        list_tasks(user_task, category)
        found_task = False
        id = int(input("Enter the ID of the task to delete: "))
        
        # Verifica se a categoria é válida
        if category not in tasks:
            print("Invalid category.")
            continue
        
        # Verifica se o ID da tarefa está dentro do intervalo de índices da lista de tarefas
        if id < 0 or id >= len(tasks[category]):
            print('Invalid ID option. Please enter a valid ID.')
            continue

        # Remove a tarefa da lista de tarefas da categoria especificada
        del tasks[category][id]
        print('Task successfully removed')
        found_task = True

        while True:
            update_another = input("Would you like to delete another task? (Y/N): ").upper()
            if update_another in ('Y', 'N'):
                break
            else:
                print('Invalid input. Please enter Y or N.')
        
        if update_another == 'N':
            break

    
# Login, verify user
def load_user_data(file_path):
    user_data = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                user_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error loading {file_path}. Starting with an empty user data.")
    return user_data


def login_user(user_data):
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")
    if username in user_data and user_data[username]['password'] == password:
        return username
    else:
        print("Invalid username or password.")
        return None



def create_account(user_data):
    while True:
        new_username = input('Please choose a username for your account:').lower()
        if new_username in user_data:
            print('Sorry, this username is already taken. Please choose another one.')
            continue
        else: 
            print("Great! This username is available.")
            while True:
                new_password = input('Please enter your password. It should contain at least 6 characters:')
                if len(new_password) < 6:
                    print("Password should contain at least 6 characters. Please try again.")
                    continue
                else:
                    user_data[new_username] = {'password': new_password, 'tasks': {'personal': [], 'business': []}}
                    save_user_data(user_data, 'users_data.json')
                    print("Account created successfully! You are now logged in.")
                    return

def save_user_data(user_data, file_path):
    # Abre o arquivo especificado em modo de escrita ('w')
    with open(file_path, 'w') as file:
        # Salva os dados do usuário (user_data) no arquivo em formato JSON
        json.dump(user_data, file)

                



        


            
        
        
        
 
# As funções restantes estão aqui, sem modificações

def main():
    file_path = 'users_data.json'
    user_data = load_user_data(file_path)
    username = login_user(user_data)
    if not username:
        became_user = input("Ready to start managing your tasks more efficiently?\n"
                        "You can easily sign up now to start organizing your tasks. Are you ready to join us? (Y/N)\n").upper()
        if became_user == 'Y':
           create_account(user_data) 

    else:
        print("Authentication successful! Welcome back,", username)    
    
    while True:
        print('Main Menu')
        print("-----------")
        print("1. Add new Task")
        print("2. List All Tasks")
        print("3. List Tasks by Category : 'Personal',  'Business')")
        print("4. Update Task")
        print("5. Delete Task(s) (select ID from menu item 2)")
        print("6. Clear screen")
        print("7. Exit application")
        
        menu_option = int(input("Please, select option between 1 and 7: "))
        
        if menu_option == 1:
            add_task(username, user_data)
        elif menu_option == 2:
            view_all_tasks(user_data)
        elif menu_option == 3:
            category = input("Enter category (P - for Personal, B - for Business): ").upper()
            if category in ['P', 'B']:
                list_tasks(user_data[username]['tasks'][category])
            else:
                print("Invalid category. Please enter P or B.")
        elif menu_option == 4:
            update_status_task(user_data[username]['tasks'])
        elif menu_option == 5:
            remove_task(user_data[username]['tasks'])
        elif menu_option == 6:
            pass  # Implemente a função clear_screen() se desejar
        elif menu_option == 7:
            save_user_data(user_data, 'users_data.json')  # Salva os dados do usuário antes de sair
            print("Exiting the application.")
            break
        else:
            print("Invalid option, please choose option between 1 and 7")


print("Welcome to your TaskManager Data Automation")   

main()
