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
    
    texto = "Task: {name}, Due Date: {due_date}, Priority: {priority}, Category: {category}, Status: {status}, Completion Date: {completion_date}"

    for p, v in enumerate(high_priority):
        print(f'High Priority Task List: {texto.format(**v)}')
        
    for p, v in enumerate(medium_priority):
        print(f'Medium Priority Task List: {texto.format(**v)}')
        
    for p, v in enumerate(low_priority):
        print(f'Low Priority Task List: {texto.format(**v)}')

#def change_task_status(tasks):

def main():
    tasks = []
    add_task(tasks)
    list_tasks(tasks)



print("Welcome to your TaskManager Data Automation")    
main() 
