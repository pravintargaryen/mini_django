from dataclasses import dataclass, field

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