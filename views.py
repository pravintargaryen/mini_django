from mini_django import HttpRequest, HttpResponse, render, render_component, render_rsc_page, broken_404,  StreamingHttpResponse, Suspense, render_suspense, SSE
from components import HomePage, UsersPage, SlowPosts
import time
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

def stream_demo(req):

    def generate():
        for i in range(5):
            yield f"<p>Streaming chunk {i}</p>"
            time.sleep(1)

    res = StreamingHttpResponse(generate())
    res.headers["Content-Type"] = "text/html"

    return res

def blog_page(req):

    def stream():

        yield "<h1>My Blog</h1>"

        suspense = Suspense(
            fallback="<p>Loading posts...</p>",
            component=SlowPosts
        )

        response = type("Temp", (), {"write": lambda self,x: chunks.append(x)})()
        chunks = []

        render_suspense(response, suspense, "posts")

        for c in chunks:
            yield c

    return StreamingHttpResponse(stream())



def events(req):

    def generate():

        i = 0

        while True:
            yield f"data: message {i}\n\n"
            i += 1
            time.sleep(1)

    return SSE(generate())

def events_page(req: HttpRequest) -> HttpResponse:
    return render(req, "events.html")    