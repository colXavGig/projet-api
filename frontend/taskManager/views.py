from django.shortcuts import render, redirect
from django.http import HttpRequest
from . import helpers
import requests as client

pages = [
    {
        'name':'Assigned tasks',
        'url':'/task/assigned-to/',
        'active':False
    },
    {
        'name':'Created tasks',
        'url':'/task/created-by/',
        'active':False
    },
    {
        'name':'Create task',
        'url':'/task/create/',
        'active':False
    }
]
# Create your views here.
def get_created_task(request: HttpRequest) :
    if 'token' not in request.session :
        return redirect('/user/login/')
    
    title = 'Created tasks'
    path = 'created-by'
    html = 'taskList.html'
    
    _pages = pages.copy()
    for page in _pages :
        if page['name'] != title :
            continue
        page['active'] = True

    if request.method == 'GET' :
        token = request.session['token']

        header = {'x-access-token':token}

        resp = client.get('http://localhost:5000/tasks/createdby/', headers=header)
        json = resp.json()
        if 'error' in json :
            return render(request, html, { 'title':title, 'pages': _pages,'error':json['error']})
        tasks = json['tasks']
        

        return render(request, html, { 'title':title, 'path':path, 'tasks':tasks, 'pages':_pages})

    return render(request, html, {'title':title, 'pages':_pages, 'error':'Method not allowed'})

def get_assigned_task(request: HttpRequest) :

    if 'token' not in request.session :
        return redirect('/user/login/')

    title = 'Assigned tasks'
    path = 'assigned-to'
    html = 'taskList.html'

    _pages = pages.copy()
    for page in _pages :
        if page['name'] != title :
            continue
        page['active'] = True

    if request.method == 'GET' :
        token = request.session['token']

        header = {'x-access-token':token}

        resp = client.get('http://localhost:5000/tasks/assignedto/', headers=header)
        json = resp.json()
        if 'error' in json :
            render(request, html, {'title':title, 'error':json['error'], 'pages':_pages})
        tasks = json['tasks']

        return render(request, html, {'title':title, 'path':path, 'tasks':tasks, 'pages':_pages})

    return render(request, html, {'title':title, 'pages':_pages})

def manage_task(request: HttpRequest, path: str, id: str) :
    print('in managed task')
    if 'token' not in request.session :
        return redirect('/auth/login/')
    
    token = request.session['token']
    header = {'x-access-token':token}
    
    if request.method == 'POST' :
        gotten = helpers.get_task(path, id, header)
        if gotten is str :
            print('not a dict: \n',gotten)
            return redirect(f"/task/{path}", {'error':gotten})
        task = gotten
        api_json = {'done':not task['done']}
        resp = client.patch(f'http://localhost:5000/tasks/{id}',headers=header, json=api_json)
        json = resp.json()
        # 
        if 'error' in json :
            print('error:', json['error'])
            return redirect(f"/task/{path}", {'error':json['error']})
        
        return redirect(f'/task/{path}')
    
    if request.method == 'GET' :
        print('GET request received')
        resp = client.delete(f'http://localhost:5000/tasks/{id}', headers=header)
        json = resp.json()
        
        if 'error' in json :
            print('got an error:', json['error'])
            return redirect(f"/task/{path}", {'error':json['error']})
        print('deleted')
        return redirect(f"/task/{path}")

    return redirect(f"/task/{path}", {"error":"Method not allowed"})

def create_task(request: HttpRequest) :
    if 'token' not in request.session :
        return redirect('/auth/login/')
    
    token = request.session['token']
    header = {'x-access-token':token}
    title = 'Create task'
    html = 'create_task.html'
    
    _pages = pages.copy()
    for page in _pages :
        if page['name'] != title :
            continue
        page['active'] = True

    if request.method == 'GET' :
         resp = client.get('http://localhost:5000/v0/users/all', headers=header)
         json = resp.json()
         if 'error' in json :
            return render(request, html, {'title':title, 'pages':_pages, 'error':json['error']})
         
         users = json['users']
         return render(request, html, {'title':title,'pages':_pages, 'users':users})
    
    if request.method == 'POST' :
        print('in POST')
        data = request.POST.dict()
        print('got data\n', data)
        resp = client.post('http://localhost:5000/tasks/', headers=header, json=data)
        print('request sent')
        json = resp.json()
        print('json response:', json)
        if 'error' in json :
            print('error:', json['error'])
            return render(request, html, { 'title':title, 'pages':_pages, 'error':json['error']})
        
        return redirect('createdBy')


        
