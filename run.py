def add_task(tasks):
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
    
    tasks.append(task)
    print('Task successfully inserted')

    return tasks

def main():
    tasks = []
    print("Welcome to your TaskManager Data Automation") 