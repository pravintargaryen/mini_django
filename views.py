from mini_django import HttpRequest, HttpResponse, render, render_component, render_rsc_page, broken_404
from components import HomePage, UsersPage

# This is similar to Django's views.py

def root(req: HttpRequest) -> HttpResponse:
    res = HttpResponse()
    res.headers['Content-Type'] = 'text/html; charset=utf-8'
    res.write("<!DOCTYPE html>");
    res.write("<html><head></head><body>")
    res.write("<p>mini_django seems to be working!</p>");
    res.write("<p>This is the page at the root path, try another path</p>")
    res.write("<p>Try /dj4e /js4e or generate errors with /missing or /broken</p>")
    res.write("</body></html>")
    return res

def dj4e(req: HttpRequest) -> HttpResponse:
    # res = HttpResponse()
    # res.headers['Content-Type'] = 'text/html; charset=utf-8'
    # res.write("<h1>Django is fun<h1>")
    # return res
    return render(req, "index.html")

def js4e(req: HttpRequest) -> HttpResponse:
    res = HttpResponse()
    res.code = "302"    # Lets do a temporary redirect...
    res.headers['Location'] = '/dj4e'
    res.headers['Content-Type'] = 'text/plain; charset=utf-8'
    res.write("You will only see this in the debugger!")
    return res

def broken(req: HttpRequest):
    return "I am a broken view, returning a string by mistake"


def home_component(req: HttpRequest) -> HttpResponse:
    return render_component(req, HomePage)


def rsc_page(req: HttpRequest) -> HttpResponse:
    return render(req, "rsc.html")

def home(req):
    return render_rsc_page(req, HomePage)    

def users(req):
    return render_rsc_page(req, UsersPage)
