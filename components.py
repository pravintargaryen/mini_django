from mini_django import h

def HomePage():
    return h("div", {"className": "container"},
        h("h1", None, "Hello from Python Server Component"),
        h("p", None, "We are returning JSX from Python 😄")
    )