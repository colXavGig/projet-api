from django.shortcuts import render, redirect, HttpResponse
import requests as req

pages = [
    {
        'name':'Login',
        'url':'/user/login/',
        'active':False
    },
    {
        'name':'Register',
        'url':'/user/signup/',
        'active':False
    }
]
# Create your views here.
def signup(request, **kwargs) :
    html = 'signup.html'
    if request.method == 'GET' :
        return render(request, html)

    if request.method == 'POST' :
        print('IN POST')

        payload = {}
        for k, v in request.POST.items() :
            payload[k] = v
        payload['name'] = payload['username']
        del payload['username']

        resp = req.post('http://localhost:5000/v0/users/signup', json=payload)
        json = resp.json()
        if 'error' in json :
            return render(request, html, {'error':json['error']})
        
        
        
        resp = req.post('http://localhost:5000/v0/users/login', json=payload)
        json = resp.json()
        
        for k, v in json.items():
            request.session[k] = v 

        return redirect('/')
        


def login_redirect(request) :
    return redirect(request,'login')

def login(request, **kwargs) :
    html = 'login.html'
    
    if request.method == 'GET' :
        return render(request, html)

    if request.method == 'POST' :
        
        payload = {}
        for k, v in request.POST.items() :
            payload[k] = v
        payload['name'] = payload['username']
        del payload['username']
        print(payload)
        
        resp = req.post('http://localhost:5000/v0/users/login', json=payload)
        json = resp.json()
        if 'error' in json :
            return render(request, html, {'error':json['error']})
        
        user = {
            'name':json['logged_user']['name'],
            'email':json['logged_user']['email'],
            'token':json['token']
        }

        for k, v in user.items() :
            print('key:', k, 'val:', v)
            request.session[k] = v

        return redirect('/')
        
        
        

        

