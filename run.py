import json #import json to transfor the data in JSON format, and can manipulate it
from datetime import datetime




def add_task():
    while True:
        name = validate_name()
        due_date = validate_date()
        priority = validate_priority()
        category = validate_category()
        description = validate_description()
        status = validate_status()
        
        task = {
            'name': name,
            'due_date': due_date,
            'priority': priority,
            'category': category,
            'description': description,
            'status': status,
            
        }

        personal = []
        business = []

        if task['category'] == 'P':
            personal.append(task)
            print('Task successfully inserted into Personal category')
        elif task['category'] == 'B':
            business.append(task)
            print('Task successfully inserted into Business category')    
        else:
            print('Invalid category')
            continue  # Volta ao início do loop externo para solicitar uma nova entrada

        return task
    

#validate date inputs
def validate_name(name):
    try:
        name = input('Enter the task name: ')
        if not name.isalpha():
            raise ValueError("Invalid name. Name should only contain alphabetic characters.")
        return name
    except ValueError as e:
        print(e)
        return None
    
def validate_date():
      try:
            due_date_str = input("Enter the due date (DD-MM-YYYY): ")
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
            return due_date.strftime("%d-%m-%Y")  # Retorna a data formatada
      except ValueError as e:
            print(e)
            print("Invalid date format. Please enter the date in the format DD-MM-YYYY.")



def validate_priority():
    try:
            priority = input('Enter the priority (low, medium, high): ').lower()
            if priority not in ['low', 'medium', 'high']:
                raise ValueError('Invalid option. Priority should be "low", "medium", or "high".')
            return priority
    except ValueError as e:
            print(f'Invalid input: {e}')



def validate_category():
    try: 
        category = input('Enter the category: P - (Personal), B - (Business)')
        if len(category) != 1 or category not in ['P', 'B']:
            raise ValueError('Category should be either "P" for Personal or "B" for Business.')
        return category 
    except ValueError as e:
        print(f'Invalid option {e} please try again.\n')
        return None


'''
validate description
'''
def validate_description():
    try:
        description = input('Enter the description: (maximum 20 characters, press Enter to skip)')
        if description == "":
            return None  # Retorna None se o usuário não fornecer uma descrição
        elif len(description) > 20:
            raise ValueError('Exceeded the input. Maximum characters allowed: 20')
        return description
    except ValueError as e:
            print(f'Invalid input: {e}')
            return None


'''
status
'''
def validate_status():
    try:
        status = input('Enter the task status : C - (Complete); P - (Pending);  IP - (In Progress): ').upper()
        if status not in ['C', 'P','IP' ]:
            raise ValueError('Status should be C - (Complete); P - (Pending);  IP - (In Progress)')
        return status
    except ValueError as e:
            print(f'Invalid input: {e}')
            return None





         


        


def list_tasks(tasks):
    high_priority = []
    medium_priority = []
    low_priority = []
    
    print('Here your tasks order by priority:')
    
    for p, v in enumerate(tasks, start=1):
        if v.get('priority') == 'high':
            high_priority.append(v)
        elif v.get('priority') == 'medium':  # Correção aqui
            medium_priority.append(v) 
        elif v.get('priority') == 'low':
            low_priority.append(v)
    
    texto = " ID : {p} Task: {name}, Due Date: {due_date}, Priority: {priority}, Category: {category}, Description: {description} Status: {status}"

    for p, v in enumerate(high_priority):
        print(f'High Priority Task List: {texto.format(**v)}')
        
    for p, v in enumerate(medium_priority):
        print(f'Medium Priority Task List: {texto.format(**v)}')
        
    for p, v in enumerate(low_priority):
        print(f'Low Priority Task List: {texto.format(**v)}')

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
                    #save_user_data(user_data)
                    print("Account created successfully! You are now logged in.")
                    return  # Sai da função após criar a conta e fazer login


def save_user_data(user_data, file_path):
    # Abre o arquivo especificado em modo de escrita ('w')
    with open(file_path, 'w') as file:
        # Salva os dados do usuário (user_data) no arquivo em formato JSON
        json.dump(user_data, file)

                



        


            
        
        
        
print("Welcome to your TaskManager Data Automation")    

