import sqlite3
from datetime import datetime
import time

# Mapeamento das categorias
CATEGORY_MAPPING = {"P": "personal", "B": "business"}
STATUS_MAPPING = {"P": "Pending", "IP": "In Progress", "C": "Complete"}


# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT
                    )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        name TEXT,
                        due_date DATE,
                        priority TEXT,
                        category TEXT,
                        description TEXT,
                        status TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )"""
    )
    conn.commit()
    return conn, cursor


# Função para registrar um novo usuário
def register_user(cursor):
    while True:
        try:
            username = input(
                "Enter username (at least 5 characters long and contain only alphanumeric characters.):"
            )
            password = input("Enter password (at least 8 characters long.): ")

            if len(username) < 5 or not username.isalnum():
                raise ValueError(
                    "Username must be at least 5 characters long and contain only alphanumeric characters."
                )
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long.")

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            cursor.connection.commit()

            print(f"User {username} registered successfully!")
            return username
        except sqlite3.IntegrityError:
            print(
                "Username already exists. Please choose a different username."
            )
        except ValueError as e:
            print(f"Error: {e}")


# Função para fazer login
def login_user(cursor):
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password),
            )
            user = cursor.fetchone()

        if user:
            print(f"Authentication successful! Welcome back, {username}")
            return username
        else:
            quit_input = input(
                'Invalid username or password. Press Enter to try again, (or type "quit" to exit):'
            ).lower()
            if quit_input.strip() == "quit":
                return None


# Funções de validação
def validate_name():
    while True:
        try:
            name = input('Enter the task name (or type "quit" to exit): ')
            if name.lower() in ["quit", "exit"]:
                return None
            if not name.strip():
                raise ValueError(
                    "Invalid name. Please provide a name, can't be empty."
                )
            if len(name) < 5:
                raise ValueError("Task name has to have at least 5 characters.")
            return name
        except ValueError as e:
            print(f"Error: {e}")


def validate_date(due_date_str):
    try:
        due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
        return due_date.strftime("%d-%m-%Y")
    except ValueError as e:
        raise ValueError(
            f"Error: {e}. Please enter the date in the format DD-MM-YYYY."
        )


def validate_priority(priority):
    if priority.lower() not in ["low", "medium", "high"]:
        raise ValueError(
            'Invalid option. Priority should be "low", "medium", or "high".'
        )
    return priority


def validate_category(category):
    if len(category) != 1 or category not in ["P", "B"]:
        raise ValueError(
            'Category should be either "P" for Personal or "B" for Business.'
        )
    return category


def validate_description(description):
    if len(description) > 50:
        raise ValueError("Exceeded the input. Maximum characters allowed: 50")
    return description


def validate_status(status):
    if status not in ["C", "P", "IP"]:
        raise ValueError(
            "Status should be C - (Complete); P - (Pending);  IP - (In Progress)"
        )
    return status


# Função para adicionar uma tarefa
def add_task(username, cursor, conn):
    while True:
        name = validate_name(
            input("Enter the task name (or type 'quit' to exit): ")
        )
        if not name:
            break

        due_date = validate_date(
            input("Enter the due date (DD-MM-YYYY) (or type 'quit' to exit): ")
        )
        if not due_date:
            break

        priority = validate_priority(
            input(
                'Enter the priority (low, medium, high) (or type "quit" to exit): '
            ).lower()
        )
        if not priority:
            break

        category = validate_category(
            input(
                'Enter the category: P - (Personal), B - (Business) (or type "quit" to exit): '
            ).upper()
        )
        if not category:
            break

        description = validate_description(
            input(
                'Enter the description: (maximum 50 characters, press Enter to skip) (or type "quit" to exit): '
            )
        )
        if description is None:
            break

        status_abbreviation = validate_status(
            input(
                'Enter the task status : C - (Complete); P - (Pending); IP - (In Progress) (or type "quit" to exit): '
            ).upper()
        )
        if status_abbreviation is None:
            break

        status = STATUS_MAPPING.get(status_abbreviation, "Unknown")

        try:
            cursor.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            )
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO tasks (user_id, name, due_date, priority, category, description, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    name,
                    due_date,
                    priority,
                    category,
                    description,
                    status,
                ),
            )

            task_id = cursor.lastrowid
            print(f"Task added successfully! Task ID: {task_id}")
            print()
            return task_id
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print("Database is locked, retrying...")
                time.sleep(2)  # Espera um pouco antes de tentar novamente
            else:
                print(f"An error occurred: {e}")
                return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


# Função para listar tarefas por categoria
def list_tasks(cursor, username, category_input):
    category = CATEGORY_MAPPING.get(category_input)
    if not category:
        print("Invalid category")
        return

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        print("User not found")
        return

    user_id = user_id[0]

    cursor.execute(
        "SELECT id, name FROM tasks WHERE user_id = ? AND category = ?",
        (user_id, category),
    )
    tasks = cursor.fetchall()

    if not tasks:
        print(f"{category.capitalize()} Tasks: None")
        return

    for task_id, task_name in tasks:
        print(f"Task ID: {task_id},  Name: {task_name}")


# Função para listar todas as tarefas
def view_all_list(cursor, username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        print("User not found")
        return

    user_id = user_id[0]

    cursor.execute(
        "SELECT id, name, category FROM tasks WHERE user_id = ?", (user_id,)
    )
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
        return

    print("All Tasks:")
    for task_id, task_name, task_category in tasks:
        print(
            f"Task ID: {task_id}, Name: {task_name}, Category: {task_category.capitalize()}"
        )


# Função para remover uma tarefa
def remove_task(cursor, task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    print("Task removed successfully!")


# Função para classificar tarefas
def sort_tasks(cursor, username):
    while True:
        print("Sort Options:")
        print("1. Sort by Due Date")
        print("2. Sort by Priority")
        print("3. Sort by Status")
        print("4. Return to Main Menu")
        option = input("Select an option: ")

        if option == "1":
            sort_by_due_date(cursor, username)
        elif option == "2":
            sort_by_priority(cursor, username)
        elif option == "3":
            sort_by_status(cursor, username)
        elif option == "4":
            break
        else:
            print("Invalid option. Please try again.")


# Função para classificar tarefas por data de vencimento
def sort_by_due_date(cursor, username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        print("User not found")
        return

    user_id = user_id[0]

    cursor.execute(
        "SELECT id, name, due_date FROM tasks WHERE user_id = ? ORDER BY due_date",
        (user_id,),
    )
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
        return

    print("Tasks Sorted by Due Date:")
    for task_id, task_name, due_date in tasks:
        print(f"Task ID: {task_id}, Name: {task_name}, Due Date: {due_date}")


# Função para classificar tarefas por prioridade
def sort_by_priority(cursor, username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        print("User not found")
        return

    user_id = user_id[0]

    cursor.execute(
        "SELECT id, name, priority FROM tasks WHERE user_id = ? ORDER BY priority",
        (user_id,),
    )
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
        return

    print("Tasks Sorted by Priority:")
    for task_id, task_name, priority in tasks:
        print(f"Task ID: {task_id}, Name: {task_name}, Priority: {priority}")


# Função para classificar tarefas por status
def sort_by_status(cursor, username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    if not user_id:
        print("User not found")
        return

    user_id = user_id[0]

    cursor.execute(
        "SELECT id, name, status FROM tasks WHERE user_id = ? ORDER BY status",
        (user_id,),
    )
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
        return

    print("Tasks Sorted by Status:")
    for task_id, task_name, status in tasks:
        print(f"Task ID: {task_id}, Name: {task_name}, Status: {status}")


# Função principal
def main():
    conn, cursor = connect_db()
    print("Welcome to Task Manager!")
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        option = input("Select an option: ")

        if option == "1":
            register_user(cursor)
        elif option == "2":
            username = login_user(cursor)
            if username:
                while True:
                    print("\nUser Menu:")
                    print("1. Add Task")
                    print("2. List Tasks by Category")
                    print("3. View All Tasks")
                    print("4. Sort Tasks")
                    print("5. Logout")
                    option = input("Select an option: ")

                    if option == "1":
                        add_task(username, cursor, conn)
                    elif option == "2":
                        category_input = input("Enter category (P/B): ").upper()
                        list_tasks(cursor, username, category_input)
                    elif option == "3":
                        view_all_list(cursor, username)
                    elif option == "4":
                        sort_tasks(cursor, username)
                    elif option == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
        elif option == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
