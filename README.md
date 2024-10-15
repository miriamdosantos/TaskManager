# Task Manager Application

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [PEP8 Validator](#pep8-validator)
- [Testing User Stories](#testing-user-stories)
  - [Client Goals](#client-goals)
  - [First Time Visitor Goals](#first-time-visitor-goals)
  - [Returning Visitor Goals](#returning-visitor-goals)
- [Manual Testing](#manual-testing)
  - [Full Testing](#full-testing)
  - [Landing Page](#landing-page)
  - [New User](#new-user)
  - [Existing User](#existing-user)
  - [Main Menu](#main-menu)
  - [Enter Task](#enter-task)
  - [Next Choice](#next-choice)
  - [Analyse Tasks](#analyse-tasks)
  - [View Tasks](#view-tasks)
- [Future Testing](#future-testing)
- [Bugs](#bugs)
  - [Resolved Bugs](#resolved-bugs)
  - [Unresolved Bugs](#unresolved-bugs)
- [Screenshots](#screenshots)
- [Credits](#credits)

## Purpose of the Project
This project is a Task Manager application designed to help users organize, manage, and track their tasks efficiently. It allows users to register, login, and interact with their personal and business tasks through an intuitive menu interface, with options to add, edit, view, sort, and remove tasks. The project integrates with Google Sheets to store user information and task details, ensuring data persistence and accessibility.
## User Stories
- 1. **User Registration**: As a new user, I want to register an account so that I can start managing my tasks.
- 2. **User Login**: As a returning user, I want to log into my account so that I can access my previously saved tasks.
- 3. **Add Task**: As a user, I want to add new tasks to my task list so that I can keep track of my activities.
- 4. **View Tasks**: As a user, I want to view all my tasks in one place so that I can easily manage my schedule.
- 5. **Edit Task**: As a user, I want to edit the details of a task so that I can update information like due date or priority.
- 6. **Remove Task**: As a user, I want to remove tasks that are no longer needed so that my task list stays organized.
- 7. **Sort Tasks**: As a user, I want to sort my tasks by: name, priority , due date or status, that I can focus on the most important ones.
- 8. **Task Categories**: As a user, I want to categorize my tasks as 'personal' or 'business' so that I can better organize my tasks.

## Colors
Colored text will be shown across the game to make users more interested and attracted. Wrong inputs across the game will be shown in red color, and green color to successuful actions. Colors in the game are imported from Python Colorama Model

## Technology Used
- **Languages**:
  - Phython

- **Libraries**
  - [Git](https://git-scm.com/)
    - Git was used for version control by utilizing the Visual Studio terminal to commit to Git and push to GitHub
  - [Github](https://github.com/)
    - GitHub is used to store the project's code after being pushed from Git
  - [Heroku](https://dashboard.heroku.com/)
    - Heroku was used to deploy the live project
  - [Draw.io](https://app.diagrams.net/)
    - Draw.io was used to creating the flowchart
  - [PEP8](https://pep8ci.herokuapp.com/#)
  - [Art] 
    - Utilized the art library to generate ASCII art for displaying titles and menus in the console, adding a visually appealing element to the application's user interface. For example, the text2art function is used to create stylized text for the "Task Manager" and "Task Menu" titles.

## Flow Chart
The planning of this project was based on the flow charts using the platform Lucid Char
<details><summary>View Screenshot</summary>![flow screenshot](./documents/task-manager-flow.jpg)



## Features

### Welcome page
![Welcome page Screenshot](./documents/welcome.png)
### 1. User Registration
Allows new users to create an account easily.
![User Registration Screenshot](screenshots/user_registration.png)

### 2. User Login
Existing users can login with their username and password.
![User Login Screenshot](screenshots/user_login.png)

### 3. Add Task
Users can add new tasks with details such as name, due date, priority, and category.
![Add Task Screenshot](screenshots/add_task.png)

### 4. View All Tasks
View all tasks in an organized list.
![View All Tasks Screenshot](screenshots/view_tasks.png)

### 5. Sort Tasks
Sort tasks based on different criteria like priority or due date for better viewing.
![Sort Tasks Screenshot](screenshots/sort_tasks.png)

### 6. Edit Task
Update the details of an existing task.
![Edit Task Screenshot](screenshots/edit_task.png)

### 7. Remove Task
Delete a task from the list, and it will be removed from Google Sheets.
![Remove Task Screenshot](screenshots/remove_task.png)

### 8. Logout
Logs the user out and returns to the login menu.
![Logout Screenshot](screenshots/logout.png)






## Installation
To install the necessary dependencies, run the following commands:
```sh
pip install colorama - The colorama library is used for colored terminal text to enhance the user interface.
pip install art - The art library is used to display ASCII art for greetings and other messages.
pip install pymemcache - The pymemcache library is used for caching user data to improve performance.
```
### Testing User Stories
#### Client Goals
- Provide an intuitive interface for managing tasks.
- Allow users to categorize and prioritize tasks.
- Ensure data persistence for user tasks.

#### First Time Visitor Goals
- Easily register and create an account.
- Understand how to add, view, and manage tasks.

#### Returning Visitor Goals
- Quickly login and access their tasks.
- Efficiently update and sort tasks.

### Manual Testing
#### Full Testing
All features were manually tested to ensure they work as expected. Below are the specific scenarios tested.
## Testing User Stories

### Client Goals
- Provide an intuitive interface for managing tasks.
- Allow users to categorize and prioritize tasks.
- Ensure data persistence for user tasks.

### First Time Visitor Goals
- Easily register and create an account.
- Understand how to add, view, and manage tasks.

### Returning Visitor Goals
- Quickly login and access their tasks.
- Efficiently update and sort tasks.

### Manual Testing
Manual testing was performed to ensure the functionality and usability of the Task Manager Application. The following scenarios were tested to confirm that each feature works as intended.

### Full Testing
All features were manually tested to ensure they work as expected. Below are the specific scenarios tested.

#### Landing Page
- **Test Case 1: Display Options**
  - Verify that the landing page displays options to register, login, or quit the application.
  - Validate that invalid inputs are handled gracefully and prompt the user to enter a valid choice.
- **Test Case 2: Quit Option**
  - Ensure the application exits when the user selects the 'Quit' option.

#### New User
- **Test Case 1: Successful Registration**
  - Register with a new username and password that meet the length requirements (at least 5 characters).
  - Ensure the user is successfully registered and redirected to the task menu.
- **Test Case 2: Username Length Validation**
  - Attempt to register with a username shorter than 5 characters.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the username.
- **Test Case 3: Password Length Validation**
  - Attempt to register with a password shorter than 5 characters.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the password.
- **Test Case 4: Existing Username Conflict**
  - Attempt to register with a username that already exists.
  - Ensure that a message indicating the username already exists is displayed and the user is prompted to choose a different username.
- **Test Case 5: Quit Registration**
  - Ensure that typing "quit" during registration returns the user to the main menu without registering.

#### Existing User
- **Test Case 1: Successful Login**
  - Login with valid credentials.
  - Ensure the user is successfully authenticated and redirected to the task menu.
- **Test Case 2: Invalid Username**
  - Attempt to login with a non-existent username.
  - Verify that an appropriate error message is displayed.
- **Test Case 3: Incorrect Password**
  - Attempt to login with an incorrect password for an existing username.
  - Verify that an appropriate error message is displayed.

#### Main Menu
- **Test Case 1: Display Options**
  - Verify that the main menu displays options to add, remove, edit, view, sort tasks, or logout.
  - Validate that invalid inputs are handled gracefully and prompt the user to enter a valid choice.
- **Test Case 2: Logout**
  - Ensure the user is returned to the login screen when selecting the 'Logout' option.

#### Enter Task
- **Test Case 1: Add Task with Valid Inputs**
  - Add a task with all required fields (name, due date, priority, category, description, status) filled correctly.
  - Ensure the task is successfully added to the appropriate category.
- **Test Case 2: Invalid Task Name**
  - Attempt to add a task with an invalid name (less than 5 characters or empty).
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the task name.

#### Enter Task
- **Test Case 3: Invalid Due Date Format**
  - Attempt to add a task with an incorrect due date format.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the due date.
- **Test Case 4: Invalid Priority**
  - Attempt to add a task with an invalid priority value.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the priority.
- **Test Case 5: Invalid Category**
  - Attempt to add a task with an invalid category value.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the category.
- **Test Case 6: Invalid Description Length**
  - Attempt to add a task with a description longer than 50 characters.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the description.
- **Test Case 7: Invalid Status**
  - Attempt to add a task with an invalid status value.
  - Verify that an appropriate error message is displayed and the user is prompted to re-enter the status.

#### Next Choice
- **Test Case 1: Add More Tasks**
  - Ensure that after adding a task, the user is prompted to add more tasks or return to the main menu.
  - Validate that choosing to add more tasks loops back to the task entry process.
- **Test Case 2: Return to Main Menu**
  - Ensure that choosing to return to the main menu correctly navigates the user back to the main menu options.

#### Analyse Tasks
- **Test Case 1: Sort by Name**
  - Sort tasks by name and verify that tasks are displayed in alphabetical order.
- **Test Case 2: Sort by Due Date**
  - Sort tasks by due date and verify that tasks are displayed in chronological order.
- **Test Case 3: Sort by Priority**
  - Sort tasks by priority and verify that tasks are displayed in the correct order (low, medium, high).
- **Test Case 4: Sort by Status**
  - Sort tasks by status and verify that tasks are displayed in the correct order (Pending, In Progress, Complete).

#### View Tasks
- **Test Case 1: Display All Tasks**
  - View all tasks and verify that tasks are displayed with all details including name, due date, priority, category, description, and status.
  - Ensure tasks are correctly grouped by category (Personal, Business).
- **Test Case 2: No Tasks**
  - Verify that an appropriate message is displayed if there are no tasks to view.

#### Future Testing
- Implement automated tests using unittest or pytest.
- Extend test coverage to include edge cases and performance testing.
- Integrated Google Calendar API
- And implementation of a properly database, I did try it but for the time and my knowlodge at the moment was not possible.

#### Bugs
#### Landing Page
- Display options to register, login, or quit the application.
- Ensure invalid input is handled gracefully.


## Bugs
### Resolved Bugs
- **Username and password length validation:** Ensured both username and password have a minimum length of 5 characters.
- **Task sorting by priority:** Fixed sorting logic to correctly order tasks by priority.

### Unresolved Bugs
- [Describe any known bugs that haven't been fixed yet.]
## Flowchart
- One popular tool for creating flowcharts is Lucidchart. It's a web-based diagramming software that allows you to create flowcharts, diagrams, and other visual representations easily.

Ilustration  the workflow of the Task Manager application, depicting the various stages such as user registration, login, task management (add, remove, edit, view, sort), and logout. Include decision points for error handling and user choices, and illustrate how the application interacts with the user and data storage
![Flow](assest/documentation/flow.jpg)
## Deployment
* Steps for deployment:
    - Fork or clone the repository
    - Create a new Keroku App
    - Set the buildpacks python and Noje.Js in that order
    - Link the Heroku app to the repository
    - Click on the deploy
    
## PEP8 Validator
I ran my code throught the Code Institute Python Linter. This showed no errors:
## Screenshots
Include relevant screenshots to illustrate the user interface and key functionalities.

### Example:
![Main Menu](screenshots/main_menu.png)
_Main Menu of the Task Manager Application_

![Add Task](screenshots/add_task.png)
_Adding a New Task_

## Credits
- Developed by [Your Name]
- Inspired by various task management applications
