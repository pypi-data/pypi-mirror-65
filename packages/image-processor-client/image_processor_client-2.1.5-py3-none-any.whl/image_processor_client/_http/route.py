from urllib.parse import quote


class Route(object):

    BASE_URL = "http://127.0.0.1:5000"

    def __init__(self, path, method: str = "POST", **params):
        self.path = path
        self.method = method
        url = self.BASE_URL + self.path
        if params:
            self.url = url.format(
                **{key: quote(value) if isinstance(value, str) else value for key, value in params.items()}
            )
        else:
            self.url = url
