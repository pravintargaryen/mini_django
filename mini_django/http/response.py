from dataclasses import dataclass, field
import json

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

    @property
    def body(self):
        return "".join(self._body)        

@dataclass
class StreamingHttpResponse(HttpResponse):
    def __init__(self, generator):
        super().__init__()
        self.generator = generator


@dataclass
class Jsonresponse(HttpResponse):
    def __init__(self, data, code=200, headers=None):
        super().__init__(code=code, headers=headers or {})  
        self.headers["Content-Type"] = "application/json" 
        self.write(json.dumps(data)) 