
from mini_django import HttpRequest, HttpResponse, view_fail, broken_404
import views

# This is similar to Django's urls.py

def router(request: HttpRequest) -> HttpResponse:
    print('==== Routing to path:', request.path);
    if request.path == '/' : 
        return views.root(request)
    elif request.path.startswith('/dj4e') : 
        return views.dj4e(request)
    elif request.path == '/js4e' : 
        return views.js4e(request)
    elif request.path == '/broken' : 
        return views.broken(request)
    elif request.path == '/rsc_page':
        return views.rsc_page(request)    
    elif request.path == '/home_component':
        return views.home_component(request)      
    elif request.path == '/home':
        return views.home(request)   
    elif request.path == '/users':
        return views.users(request)      
    elif request.path == "/404":
        return broken_404(request, "404")         

    # When all else fails send the 404 screen
    else :
        return view_fail(request, "404", "urls.py could not find a view for the path")

