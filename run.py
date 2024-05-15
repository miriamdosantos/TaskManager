def add_task():
    name = input('Enter the task name: ')
    due_date = input('Enter the due date (YYYY-MM-DD): ')
    priority = input('Enter the priority (low, medium, high): ')
    category = input('Enter the category: P - (Personal), B - (Business)')
    description = input('Enter the description: ')
    status = input('Enter the status (C - complete, P - pending, I - in progress): ')
    assignee = input('Enter the assignee: ')
    completion_date = input('Enter the completion date (YYYY-MM-DD): ')
    
    task = {
        'name': name,
        'due_date': due_date,
        'priority': priority,
        'category': category,
        'description': description,
        'status': status,
        'assignee': assignee,
        'completion_date': completion_date
    }
    personal=[]
    business=[]

    if task['category'] == 'P':
        personal.append(task)
        print('Task successfully inserted into Personal category')
    elif task['category'] == 'B':
        business.append(task)
        print('Task successfully inserted into Business category')    
    else:
        print('Invalid category')
        return False


    return task

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
    
    texto = " ID : {p} Task: {name}, Due Date: {due_date}, Priority: {priority}, Category: {category}, Status: {status}, Completion Date: {completion_date}"

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
    

        
        


            
        
        
        
print("Welcome to your TaskManager Data Automation")    

