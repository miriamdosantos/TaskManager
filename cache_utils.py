import memcache
import os
import json

# Configure Memcached
memcached_servers = os.getenv('MEMCACHIER_SERVERS', 'localhost:11211')
memcached_username = os.getenv('MEMCACHIER_USERNAME', '')
memcached_password = os.getenv('MEMCACHIER_PASSWORD', '')

# Build the connection string with authentication
if memcached_username and memcached_password:
    memcached_servers_with_auth = f'{memcached_username}:{memcached_password}@{memcached_servers}'
else:
    memcached_servers_with_auth = memcached_servers

# Connect to Memcached
mc = memcache.Client([memcached_servers_with_auth], debug=0)


def set_user_tasks(username, tasks):
    mc.set(username, json.dumps(tasks))

def get_user_tasks(username):
    user_tasks = mc.get(username)
    if not user_tasks:
        return {'personal': [], 'business': []}
    return json.loads(user_tasks)

def save_data(username, users):
    # Atualizar o cache com os dados do usuário
    user_tasks = users.get(username, {}).get('tasks', {})
    set_user_tasks(username, user_tasks)

    # Escrever os dados em um arquivo JSON
    with open('users_data.json', 'w') as file:
        json.dump(users, file, indent=4)
    # Escrever os dados em um arquivo JSON
    with open('users_data.json', 'w') as file:
        json.dump(users, file, indent=4)
