from html.parser import HTMLParser
from mini_django import HttpRequest, HttpResponse
import json 


class JSXParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.root = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k: v for (k, v) in attrs}
        # ⭐ ngIf support
        if "*ngIf" in attrs_dict:
            condition = attrs_dict.pop("*ngIf")
            if not eval(condition, self.context):
                self.skip_tag = tag
                return
        if "*ngFor" in attrs_dict:
            expr = attrs_dict.pop("*ngFor")
            # "let user of users"
            var_name, iterable_name = expr.replace("let ", "").split(" of ")

            iterable = eval(iterable_name, self.context)
            parent = self.stack[-1] if self.stack else None

            for item in iterable:
                self.context[var_name.strip()] = item
                clone_attrs = [(k,v) for k,v in attrs if k != "*ngFor"]
                self.handle_starttag(tag, clone_attrs)
                self.handle_endtag(tag)
                return        

        #React        
        props = {k: v for (k, v) in attrs}
        if tag[0].isupper():
            element = {
        "type": "CLIENT_COMPONENT",
        "name": tag,
        "props": props,
        "children": []
            }
        else:
            element = {
        "type": tag,
        "props": props,
        "children": []
            }

        if self.stack:
            self.stack[-1]["children"].append(element)
        else:
            self.root = element

        self.stack.append(element)

    def handle_endtag(self, tag):
        self.stack.pop()
        if getattr(self, "skip_tag", None) == tag:
            self.skip_tag = None
            return

    def handle_data(self, data):
        text = data.strip()
        if text and self.stack:
            self.stack[-1]["children"].append(text)  

def compile_jsx(jsx_string: str):
    parser = JSXParser()
    parser.feed(jsx_string.strip())
    return parser.root

def jsx(func):
    def wrapper(*args, **kwargs):
        jsx_string = func(*args, **kwargs)
        return compile_jsx(jsx_string)
    return wrapper   


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