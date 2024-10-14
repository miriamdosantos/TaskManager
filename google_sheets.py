import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt

def setup_google_sheets(sheet_name="Task-Manager", sheet_index=0):
    """
    Set up the Google Sheets API client using credentials and return the specified sheet.

    Args:
        sheet_name (str): The name of the Google Sheet (default is "Task-Manager").
        sheet_index (int): Index of the worksheet to access (default is 0).

    Returns:
        gspread.models.Worksheet: The specified worksheet, or None if an error occurs.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Check if credentials are provided as an environment variable or in a local JSON file
    creds_json = os.environ.get("GOOGLE_SHEET_CREDENTIALS")
    if creds_json:
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json), scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    try:
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).get_worksheet(sheet_index)  # Access the worksheet by index
        return sheet
    except gspread.SpreadsheetNotFound:
        print(f"Error: The spreadsheet '{sheet_name}' was not found.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def load_data_from_sheet():
    """
    Load user and task data from Google Sheets.

    Returns:
        dict: A dictionary containing user data and their tasks.
    """
    user_sheet = setup_google_sheets("Task-Manager", 0)  # Load the user worksheet (index 0)
    task_sheet = setup_google_sheets("Task-Manager", 1)  # Load the task worksheet (index 1)

    if user_sheet is None or task_sheet is None:
        print("Error: Unable to access Google Sheets.")
        return {}

    # Load user data
    user_data = user_sheet.get_all_records()
    users_data = {}
    
    for record in user_data:
        if 'Username' in record:
            username = record['Username']
            password = record['Password']

            if username not in users_data:
                users_data[username] = {
                    "password": password,
                    "tasks": {
                        "personal": [],
                        "business": []
                    }
                }

    # Load task data
    task_data = task_sheet.get_all_records()
    
    for record in task_data:
        if 'Username' in record:
            username = record['Username']
            task = {
                "name": record['Task Name'],
                "due_date": record['Due Date'],
                "priority": record['Priority'],
                "category": record['Category'],
                "description": record['Description'],
                "status": record['Status']
            }
            if username in users_data and task["category"] in users_data[username]["tasks"]:
                users_data[username]["tasks"][task["category"]].append(task)

    return users_data

def save_data_to_sheet(users_data):
    """
    Save user and task data back to Google Sheets.

    Args:
        users_data (dict): Dictionary containing user data and their tasks.
    """
    user_sheet = setup_google_sheets("Task-Manager", 0)  # Load the user worksheet
    task_sheet = setup_google_sheets("Task-Manager", 1)  # Load the task worksheet

    if user_sheet is None or task_sheet is None:
        print("Error: Unable to access Google Sheets.")
        return

    # Update the user worksheet
    existing_users = {record['Username'] for record in user_sheet.get_all_records()}

    # Add header to the user sheet if it is empty
    if not existing_users:
        user_sheet.append_row(["Username", "Password"])  # Add header

    for username, user_info in users_data.items():
        if username not in existing_users:
            user_sheet.append_row([username, user_info["password"]])
            existing_users.add(username)

    # Update the task worksheet
    existing_tasks = set((record['Username'], record['Task Name'], record['Due Date']) 
                         for record in task_sheet.get_all_records())

    # Add header to the task sheet if it is empty
    if not existing_tasks:
        task_sheet.append_row(["Username", "Task Name", "Due Date", "Priority", "Category", "Description", "Status"])

    for username, user_info in users_data.items():
        for category, tasks in user_info["tasks"].items():
            for task in tasks:
                task_id = (username, task["name"], task["due_date"])
                
                if task_id not in existing_tasks:
                    task_sheet.append_row([
                        username,
                        task["name"],
                        task["due_date"],
                        task["priority"],
                        category,
                        task["description"],
                        task["status"]
                    ])
                    existing_tasks.add(task_id)
