import json

import aiohttp.web


class GoodResponse(aiohttp.web.Response):
    def __init__(self, result, status_code=200, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = json.dumps({"result": result})
        self._status = status_code
        self.content_type = "application/json"


class BadResponse(aiohttp.web.Response):
    def __init__(self, result, status_code=400, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = json.dumps({"error": result})
        self._status = status_code
        self.content_type = "application/json"
