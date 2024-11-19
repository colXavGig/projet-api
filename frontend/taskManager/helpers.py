import requests as client

def get_task(path: str, id: str, header: dict) :
    path = 'createdby' if path == 'created-by' else 'assignedto'
    url = f'http://localhost:5000/tasks/{path}'
    
    resp = client.get(url, headers=header)
    json = resp.json()
    
    if 'error' in json :
        return json['error']
    
    tasks: list = json['tasks']
    task: dict
    for t in tasks :
        if t['id'] == id :
            task = t
            break
    return task