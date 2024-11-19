from django.shortcuts import render, redirect

task_pages = [
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

connection_pages = [
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
#


# Create your views here.
def home(request) :
    _pages: list
    if 'token' not in request.session :
        _pages = connection_pages        
    else :
        _pages = task_pages
    return render(request, 'home.html', {'pages':_pages})