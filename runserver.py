import mini_django
import sys
import urls

port = 9000
if len(sys.argv) > 1 :
    port = int(sys.argv[1])

print('Access http://localhost:'+str(port))
mini_django.httpServer(urls.router, port)

