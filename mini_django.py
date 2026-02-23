# https://docs.python.org/3/howto/sockets.html
# https://stackoverflow.com/questions/8627986/how-to-keep-a-socket-open-until-client-closes-it
# https://stackoverflow.com/questions/10091271/how-can-i-implement-a-simple-web-server-using-python-without-using-any-libraries

from socket import *
import traceback, json
from dataclasses import dataclass
from dataclasses import field
import sys

@dataclass
class HttpRequest:
    method: str = ""
    path: str = ""
    headers: dict = field(default_factory=dict)
    body: str = ""

@dataclass
class HttpResponse:
    code: str = "200"
    headers: dict = field(default_factory=dict)
    _body: list = field(default_factory=list)

    def write(self, line: str) :
        self._body.append(line)
    def write_html(self, html: str):
        with open(html, "r") as file:
            self._body.append(file.read())


def parseRequest(rd:str) -> HttpRequest:
    retval = HttpRequest()
    retval.body = rd
    ipos = rd.find("\r\n\r\n")
    if ipos < 1 : 
        print('Incorrectly formatted request input')
        print(repr(rd))
        return None

    # Find the blank line between HEAD and BODY
    head = rd[0:ipos-1]
    lines = head.split("\n")

    # GET / HTTP/1.1
    if len(lines) > 0 :
        firstline = lines[0]
        pieces = firstline.split(' ')
        if len(pieces) >= 2 :
            retval.method = pieces[0] or 'Missing'
            retval.path = pieces[1] or 'Missing'

    # Accept-Language: en-US,en;q=0.5
    for line in lines:
        line = line.strip()
        pieces = line.split(": ", 1)
        if len(pieces) != 2 : continue
        retval.headers[pieces[0].strip()] = pieces[1].strip()
    return retval

def responseSend(clientsocket, response: HttpResponse) :

    try:
        print('==== Sending Response Headers')
        firstline = "HTTP/1.1 "+str(response.code)+" OK\r\n"
        clientsocket.sendall(firstline.encode())
        for key, value in response.headers.items():
            print(key+': '+value)
            clientsocket.sendall(key.encode())
            clientsocket.sendall(": ".encode())
            clientsocket.sendall(value.encode())
            clientsocket.sendall("\r\n".encode())
    

        clientsocket.sendall("\r\n".encode())
        chars = 0
        for line in response._body:
            line = patchAutograder(line)

            chars += len(line)
            clientsocket.sendall(line.replace("\n", "\r\n").encode())
            clientsocket.sendall("\r\n".encode())
        print("==== Sent",chars,"characters body output")

    except Exception as exc :
        print(exc)
        print(response)
        print(traceback.format_exc())

# If we are sending HTML, optionally include the endpoint for the DJ4E JavaScript autograder

# If you want to include the autograder library run this as follows:
# python runserver.py 9000 autograder

# To use a local copy of the autograder library, run as follows:
# python runserver.py 9000 http://localhost:8888/dj4e/tools/jsauto/autograder.js

def patchAutograder(line: str) -> str:
    if len(sys.argv) < 3 : return line
    if line.find('</body>') == -1 : return line
    if sys.argv[2] == "autograder" :
        dj4e_autograder = "https://www.dj4e.com/tools/jsauto/autograder.js"
    else:
        dj4e_autograder = sys.argv[2]
    return line.replace('</body>', '\n<script src="'+dj4e_autograder+'"></script>\n</body>')

def httpServer(router, port):
    print('\n================ Starting mini_django server on '+str(port))
    serversocket = socket(AF_INET, SOCK_STREAM)
    try :
        serversocket.bind(('localhost',port))
        serversocket.listen(5)
        while(1):
            print('\n================ Waiting for the Next Request')
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            print('====== Received Headers')
            print(rd)
            request = parseRequest(rd)

            # If we did not get a valid request, send a 500
            if not isinstance(request, HttpRequest) :
                response = view_fail(request, "500", "Request could not be parsed")

            # Send valid request to the router (urls.py)
            else:
                response = router(request)

                # If we did not get a valid response, log it and send back a 500
                if not isinstance(response, HttpResponse) :
                    response = view_fail(request, "500", "Response returned from router / view is not of type HttpResponse")

            try:
                responseSend(clientsocket, response)
                clientsocket.shutdown(SHUT_WR)
            except Exception as exc :
                print(exc)
                print(traceback.format_exc())

    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print(exc)
        print(traceback.format_exc())

    print("Closing socket")
    serversocket.close()

def view_fail(req: HttpRequest, code: str, failure: str) -> HttpResponse:
    res = HttpResponse()
    method = req.method if req else "UNKNOWN"
    print(" ")
    print("Sending view_fail, code="+code+" failure="+failure)

    res.code = code

    res.headers['Content-Type'] = 'text/html; charset=utf-8'

    res.write("<!DOCTYPE html>");
    res.write('<html><body>')
    if res.code == "404" :
        res.write('<div style="background-color: rgb(255, 255, 204);">')
    else :
        res.write('<div style="background-color: pink;">')

    res.write('<b>Page has errors</b>')
    res.write('<div><b>Request Method:</b> ' + method + "</div>")
    res.write('<div><b>Request URL:</b> '+req.path+'</div>')
    res.write('<div><b>Response Failure:</b> '+failure+'</div>')
    res.write('<div><b>Response Code:</b> '+res.code+'</div>')
    res.write("</div><pre>")
    res.write("Valid paths: /dj4e /js4e or /404")
    res.write("\nRequest header data:")
    res.write(json.dumps(req.headers, indent=4))
    res.write("</pre></body></html>")
    return res


def render(req: HttpRequest, template_name: str) -> HttpResponse:
    res = HttpResponse()
    res.code = 200
    res.headers['Content-Type'] = 'text/html; charset=utf-8'
    res.write_html(template_name)
    return res

def h(tag, props=None, *children):
    normalized_children = []

    for child in children:
        if child is None:
            continue
        elif isinstance(child, list):
            normalized_children.extend(child)
        else:
            normalized_children.append(child)

    return {
        "type": tag,
        "props": props or {},
        "children": normalized_children
    }

    
def render_component(req: HttpRequest, component_func) -> HttpResponse:
    tree = component_func()
    json_string = json.dumps(tree)

    res = HttpResponse()
    res.code = "200"
    res.headers['Content-Type'] = 'application/json; charset=utf-8'

    # ⭐ THIS is the correct way in your framework
    res.write(json_string)

    return res

def render_rsc_page(req: HttpRequest, component_func) -> HttpResponse:
    tree = component_func()
    json_payload = json.dumps(tree)

    res = HttpResponse()
    res.code = "200"
    res.headers['Content-Type'] = 'text/html; charset=utf-8'

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
</head>
<body>

<div id="root">Loading...</div>

<script>
  const SERVER_COMPONENT = {json_payload};

  function createElementFromJSON(node) {{
    if (typeof node === "string") return node;
    return React.createElement(
      node.type,
      node.props,
      ...node.children.map(createElementFromJSON)
    );
  }}

  const root = ReactDOM.createRoot(document.getElementById("root"));
  const component = createElementFromJSON(SERVER_COMPONENT);
  root.render(component);
</script>

</body>
</html>
"""

    res.write(html)
    return res    

def broken_404(req:HttpRequest , code:str) -> HttpResponse:
    res = HttpResponse()
    method = req.method if req else "UNKNOWN"
    res.code = code
    res.headers['Content-Type'] = 'text/html; charset=utf-8'
    res.write("<!DOCTYPE html>");
    res.write('<html><body>')    
    res.write('<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjJLm8EZ2mlaDVgGihyFt_qFn9reeV8wp0mxBDunJSFPYJaTEiazBbfYYL80Tr7xjO8n1rS4EEXEm-Uj6P3yD3YuiL0_JDw53gOBG4HEwVoJhOgma7oPIhub3cTlwp3jSswU0F1ow/s640/google-error-page-2011.png" />')
    res.write("</body></html>")    
    return res    