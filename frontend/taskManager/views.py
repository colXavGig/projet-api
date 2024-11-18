from django.shortcuts import render, redirect
import requests as client

# Create your views here.
def get_created_task(request) :
    if 'token' not in request.session :
        print('no token')
        print(request.session)
        return redirect('/user/login/')

    html = 'created_taskList.html'

    if request.method == 'GET' :
        token = request.session['token']

        header = {'x-access-token':token}

        resp = client.get('http://localhost:5000/tasks/createdby/', headers=header)
        json = resp.json()
        if 'error' in json :
            return render(request, html, {'error':json['error']})
        print(json)
        tasks = json['tasks']
        

        return render(request, html, {'tasks':tasks})

    return render(request, html)

def get_assigned_task(request) :

    if 'token' not in request.session :
        return redirect('/user/login/')

    html = 'assigned_taskList.html'

    if request.method == 'GET' :
        token = request.session['token']

        header = {'x-access-token':token}

        resp = client.get('http://localhost:5000/tasks/assignedto/', headers=header)
        json = resp.json()
        if 'error' in json :
            render(request, html, error=json['error'])
        tasks = json['tasks']
        print('tasks: ', tasks)

        return render(request, html, {'tasks':tasks})

    return render(request, html)

def manage_task(request, path, id ) :
    if 'token' not in request.session :
        
        return redirect('/auth/login/')
    
    token = request.session['token']
    header = {'x-access-token':token}
    
    if request.method == 'PATCH' :
        resp = client.patch(f'http://localhost:5000/tasks/{id}',headers=header)
        json = resp.json()
        
        if 'error' in json :
            return redirect(path, error=json['error'])
        
        return redirect(path)
    
    if request.method == 'DELETE' :
        resp = client.patch(f'http://localhost:5000/tasks/{id}',headers=header)
        json = resp.json()
        
        if 'error' in json :
            return redirect(path, error=json['error'])
        
        return redirect(path)

    return redirect(path, error="Method not allowed")

