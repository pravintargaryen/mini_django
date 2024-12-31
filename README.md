
Mini Django Web Server
======================

This is a very small Python web server that takes inspiration from Django.  To
run this server, type:

    python runserver.py

And navigate to http://localhost:9000

If you want a port other than 9000, add it as an additional parameter on the
`runserver` command.

Looking at Code
---------------

`mini_django.py`

`runserver.py`

`urls.py`

`views.py`


Development
-----------

Running with a local copy of the autograder JavaScript.

    python runserver.py 9000 http://localhost:8888/dj4e/tools/jsauto/autograder.js

