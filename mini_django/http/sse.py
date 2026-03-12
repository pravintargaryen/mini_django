from mini_django import StreamingHttpResponse

class SSE(StreamingHttpResponse):

    def __init__(self, generator):
        super().__init__(generator)

        self.headers["Content-Type"] = "text/event-stream"
        self.headers["Cache-Control"] = "no-cache"
        self.headers["Connection"] = "keep-alive"