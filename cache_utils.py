import memcache
import os
import json

# Configure Memcached
memcached_servers = os.getenv("MEMCACHIER_SERVERS", "localhost:11211")
memcached_username = os.getenv("MEMCACHIER_USERNAME", "")
memcached_password = os.getenv("MEMCACHIER_PASSWORD", "")

# Build the connection string with authentication
if memcached_username and memcached_password:
    memcached_servers_with_auth = (
        f"{memcached_username}:{memcached_password}@{memcached_servers}"
    )
else:
    memcached_servers_with_auth = memcached_servers

# Connect to Memcached
mc = memcache.Client([memcached_servers_with_auth], debug=0)


# Connect to Memcached
mc = memcache.Client([memcached_servers_with_auth], debug=0)


# Set user tasks in Memcached
def set_user_tasks(username, tasks):
    """
    Set user tasks in Memcached.

    Parameters:
        username (str): Username of the user.
        tasks (dict): Dictionary containing user tasks.

    Returns:
        None
    """
    mc.set(username, json.dumps(tasks))


# Get user tasks from Memcached


def get_user_tasks(username):
    """
    Get user tasks from Memcached.

    Parameters:
        username (str): Username of the user.

    Returns:
        dict: Dictionary containing user tasks.
    """
    user_tasks = mc.get(username)
    if not user_tasks:
        return {"personal": [], "business": []}
    return json.loads(user_tasks)


# Save user data to JSON file and update Memcached
def save_data(username, users):
    user_tasks = users.get(username, {}).get("tasks", {})
    set_user_tasks(username, user_tasks)
    # Write data to a JSON file
    with open("users_data.json", "w") as file:
        json.dump(users, file, indent=4)
