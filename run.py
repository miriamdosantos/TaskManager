import json #import json to transfor the data in JSON format, and can manipulate it
from datetime import datetime



from datetime import datetime

def add_task():
    personal = []
    business = []

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
            personal.append(task)
            print('Task successfully inserted into Personal category')
        elif category == 'B':
            business.append(task)
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

    return personal, business


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








         


        


def list_tasks(tasks, category):
    # Crie listas vazias para cada categoria e prioridade
    high_priority = []
    medium_priority = []
    low_priority = []
    
    # Separe as tarefas por prioridade
    for task in tasks:
        if task['category'] == category:
            if task['priority'] == 'high':
                high_priority.append(task)
            elif task['priority'] == 'medium':
                medium_priority.append(task)
            elif task['priority'] == 'low':
                low_priority.append(task)
                
    # Exiba as tarefas
    # Imprima as tarefas separadas por prioridade
    print(f"{category.capitalize()} Tasks:")
    print("High Priority:")
    for task in high_priority:
        print(task)
    print("Medium Priority:")
    for task in medium_priority:
        print(task)
    print("Low Priority:")
    for task in low_priority:
        print(task)

    print('Sort Options')
# Loop do menu de opções
    while True:
        print("Sort Options:")
        print("1. By Due Date (closest first)")
        print("2. By Due Date (farthest first)")
        print("3. By Status")
        print("4. Exit")
        
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
            print('High Priority - Due Date:')
            print_task_details(sort_by_due_date(high_priority))
            print('Medium Priority - Due Date:')
            print_task_details(sort_by_due_date(medium_priority))
            print('Low Priority - Due Date:')
            print_task_details(sort_by_due_date(low_priority))
        elif sort_option == 2:
            print('High Priority - Due Date:')
            print_task_details(sort_by_due_date(high_priority, reverse=True))
            print('Medium Priority - Due Date:')
            print_task_details(sort_by_due_date(medium_priority, reverse=True))
            print('Low Priority - Due Date:')
            print_task_details(sort_by_due_date(low_priority, reverse=True))
        elif sort_option == 3:
            print('High Priority - Status:')
            print_task_details(sort_by_status(high_priority))
            print('Medium Priority - Status:')
            print_task_details(sort_by_status(medium_priority))
            print('Low Priority - Status:')
            print_task_details(sort_by_status(low_priority))
        elif sort_option == 4:
            print("Exiting the program.")
            break  # Sai do loop do menu


def print_task_details(task):
    # Função para imprimir os detalhes de uma tarefa
    print(f"Name: {task['name']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Priority: {task['priority']}")
    print(f"Status: {task['status']}")
    print(f"Description: {task['description']}")
    print()
    
def sort_by_due_date(tasks, order):
    # Listas para armazenar as tarefas ordenadas
    tasks_sorted = []
    tasks_sorted_last = []
    
    # Itera sobre todas as tarefas
    for task in tasks:
        # Obtém a data de vencimento da tarefa
        due_date = task.get('due_date', 'Not found')
        
        # Adiciona a tarefa à lista de tarefas ordenadas com base na data de vencimento
        if order == 1:
            tasks_sorted.append(task)
        elif order == 2:
            tasks_sorted_last.append(task)
    
    # Ordena as listas de tarefas com base na data de vencimento
    tasks_sorted = sorted(tasks_sorted, key=lambda x: x['due_date'])
    tasks_sorted_last = sorted(tasks_sorted_last, key=lambda x: x['due_date'], reverse=True)

    return tasks_sorted, tasks_sorted_last


def sort_by_status(tasks):
    for task in tasks:
        status=task.get('status', 'Not found')
        tasks_sorted = sorted(tasks,key=lambda x: x['stuatus'] == ['I','P','C'] )
    return tasks_sorted

        
        



def update_status_task(tasks):
    while True:
        list_tasks(tasks)
        id = int(input("Enter the ID of the task to update the status: "))
        
        found_task = False
        for p, v in enumerate(tasks):
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

def remove_task(tasks):
    while True:
        list_tasks(tasks)
        found_task = False
        id = int(input("Enter the ID of the task to delete: "))
        for p,v in enumerate (tasks):
            if id == p:
                del tasks[p]
                print('Task successfuly removed')
                found_task = True
                break
            
        if not found_task:
            print('Invalid ID option. Please enter a valid ID.')
            continue
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
    try:
        with open(file_path, 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}  # Se o arquivo não existe, comece com um dicionário vazio
    return user_data

def login_user():
    user_data = load_user_data()
    user_name = input("Enter your UserName:")
    password = input("Enter your password: ")
    if user_name in user_data:
        if user_data[user_name]['password'] == password:
            print("Authentication successful!")
            return True
        else:
            print("Incorrect password.")
    else:
        print("User not found.")
    return False


def create_account():
    while True:
        user_data = load_user_data()
        new_username = input('Please choose a username for your account:').lower()
        if new_username in user_data:
            print('Sorry, this username is already taken. Please choose another one.')
            continue  # Volta ao início do loop externo para pedir um novo nome de usuário
        else: 
            print("Great! This username is available.")
            while True:
                new_userpassword = input('Please enter your password. It should contain at least 6 characters:')
                if len(new_userpassword) < 6:
                    print("Password should contain at least 6 characters. Please try again.")
                    continue  # Volta ao início do loop interno para pedir uma nova senha
                else:
                    user_data.update({new_username: {"password": new_userpassword}})                    
                    save_user_data(user_data)
                    print("Account created successfully! You are now logged in.")
                    return  # Sai da função após criar a conta e fazer login


def save_user_data(user_data, file_path):
    # Abre o arquivo especificado em modo de escrita ('w')
    with open(file_path, 'w') as file:
        # Salva os dados do usuário (user_data) no arquivo em formato JSON
        json.dump(user_data, file)

                



        


            
        
        
        
print("Welcome to your TaskManager Data Automation")    

