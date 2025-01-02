
Mini Django Web Server
======================

This is a very small Python web server that takes inspiration from Django.  To
run this server, type:

    python runserver.py

And navigate to http://localhost:9000

If you want the server to listen on a port other than 9000, add it as an additional parameter on the
`runserver` command.

    python runserver.py 9001

And navigate to http://localhost:9001

Looking at Code
---------------

`mini_django.py`

This file is about 200 lines of Python and approximates the entire Django library in a very simple way.  It
handles many aspects of the <a href="https://en.wikipedia.org/wiki/HTTP" target="_blank:">HTTP Network Protocol</a>
like parsing incoming requests, calling your "application router", and sending a correctly formatted the HTTP response
back to the browser to complete the request/response cycle.  This library also defines `HttpRequest` and
`HttpResponse` data classes which are passed into and returned from the application views.

`runserver.py`

This is a very short file.  It loads the `mini_django` library and calls the `httpServer` method
to start listening for connections on the specified port.

`urls.py`

The purpose of this file is to look at the `path` value from the `HttpRequest` object and decide which view
to call.  In "real Django", the paths are stored in an array, but to make easier to understand, this file just
uses a series if `if-then-else` tests to pick the correct view for the path.

`views.py`

This is very similar to the `views.py` in "real Django".  Each view is a function that takes an `HttpRequest`
as its parameter and returns an `HttpResponse` as its return value.  In each view, the code creates
an `HttpResponse` and sets headers in the response and adds the body text to the response and then 
returns it to `mini_django` which then correctly formats the response and sends it back to the browser
to complete the request / response cycle.

AutoGrader Support
------------------

As this code is part of the <a href="https://www.dj4e.com/" target="_blank">Django for Everybody</a>
course, it includes a small JavaScript library to enable this code to be autograded as an assignment
for the course.  Take a look at the `patchAutograder()` method in `mini_django` for details.

The autograder library is only included in `text/html` responses.

If you want to run this without including the autograder run the program as follows:

    python ruserver.py 9000 none

You can also do development with a local copy of the autograder JavaScript as follows:

    python runserver.py 9000 http://localhost:8888/dj4e/tools/jsauto/autograder.js

