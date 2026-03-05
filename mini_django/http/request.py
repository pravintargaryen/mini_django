from dataclasses import dataclass, field

@dataclass
class HttpRequest:
    method: str = ""
    path: str = ""
    headers: dict = field(default_factory=dict)
    body: str = ""
