from mini_django import HttpRequest, HttpResponse

def render(req: HttpRequest, template_name: str) -> HttpResponse:
    res = HttpResponse()
    res.code = 200
    res.headers['Content-Type'] = 'text/html; charset=utf-8'
    res.write_html(template_name)
    return res