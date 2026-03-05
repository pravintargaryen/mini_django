from html.parser import HTMLParser
import re

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

def ng_component(func):
    def wrapper(*args, **kwargs):
        html = func(*args, **kwargs)
        context = func.__globals__.copy()
        return compile_ng_template(html, context)
    return wrapper


def interpolate(text, context):
    pattern = r"{{\s*(.*?)\s*}}"

    def repl(match):
        expr = match.group(1)
        try:
            return str(eval(expr, context))
        except:
            return ""

    return re.sub(pattern, repl, text)    


def compile_ng_template(template: str, context: dict):
    parser = JSXParser()
    parser.context = context
    template = interpolate(template, context)
    parser.feed(template.strip())
    return parser.root   