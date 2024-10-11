import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_google_sheets(sheet_name="Task-Manager"):
    """
    Set up the Google Sheets API client using credentials and return the specified sheet.

    Args:
        sheet_name (str): The name of the Google Sheet (default is "Task-Manager").

    Returns:
        gspread.models.Worksheet: The first sheet of the spreadsheet if successful, None if an error occurs.
    """
    # Define the scope for accessing Google Sheets and Google Drive
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Check if we are running on Heroku or locally
    if os.environ.get("HEROKU") == "True":
        # Load credentials from the environment variable
        creds_json = os.environ.get("GOOGLE_SHEET_CREDENTIALS")
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json), scope)
    else:
        # Load credentials from a JSON keyfile locally
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    try:
        client = gspread.authorize(creds)  # Authorize the client using credentials
        sheet = client.open(sheet_name).sheet1  # Open the first sheet in the spreadsheet
        return sheet
    except gspread.SpreadsheetNotFound:
        print(f"Error: The spreadsheet '{sheet_name}' was not found.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
   
def load_data_from_sheet():
    """
    Load user data and tasks from the Google Sheet into a dictionary.

    Returns:
        dict: A dictionary containing user data (username, hashed password) and their tasks.
    """
    sheet = setup_google_sheets()
    if sheet is None:
        return {}  # Return an empty dictionary if the sheet could not be loaded

    # Get all records from the sheet as a list of dictionaries
    records = sheet.get_all_records()
    users_data = {}

    # Process each record in the sheet
    for record in records:
        username = record['username']
        password = record['password']  # The password is already hashed in the sheet
        category = record['category']

        # Initialize the user's data structure if not already done
        if username not in users_data:
            users_data[username] = {
                "password": password,
                "tasks": {
                    "personal": [],
                    "business": []
                }
            }

        # Build the task dictionary from the record
        task = {
            "name": record['task_name'],
            "due_date": record['due_date'],
            "priority": record['priority'],
            "description": record['description'],
            "status": record['status'],
        }
        
        # Append the task to the corresponding category (personal or business)
        if category == "personal":
            users_data[username]["tasks"]["personal"].append(task)
        elif category == "business":
            users_data[username]["tasks"]["business"].append(task)

    return users_data  # Return the complete user data dictionary

def save_data_to_sheet(users_data):
    """
    Save user data and their tasks back to the Google Sheet.

    Args:
        users_data (dict): A dictionary containing user data (username, hashed password) and their tasks.
    """
    sheet = setup_google_sheets()
    
    if sheet is None:
        print("Error: Unable to access Google Sheet.")
        return

    # Clear the sheet to remove old data before saving the new data
    sheet.clear()

    # Write the header row to the sheet
    sheet.append_row(["username", "password", "task_name", "due_date", "priority", "category", "description", "status"])

    # Iterate through the users and their respective data
    for username, user_info in users_data.items():
        # Write the username and hashed password to the sheet
        sheet.append_row([username, user_info["password"], "", "", "", "", "", ""])

        # Loop through the task categories (personal, business)
        for category, tasks in user_info["tasks"].items():
            # Save each task under the correct category
            for task in tasks:
                sheet.append_row([
                    username,
                    "",  # Password is not duplicated here for tasks
                    task["name"],
                    task["due_date"],
                    task["priority"],
                    category,
                    task["description"],
                    task["status"]
                ])
