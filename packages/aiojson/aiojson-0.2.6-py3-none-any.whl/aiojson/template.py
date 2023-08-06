from functools import wraps

import aiohttp.web_request

from aiojson.exception import ApiException
from aiojson.response import GoodResponse, BadResponse


class WrongDataType(ApiException):
    def __init__(self, path):
        super().__init__(f"Wrong data passed in {path}.")


class DataMissing(ApiException):
    def __init__(self, path):
        super().__init__(f"Required data missing at {path}.")


class JsonTemplate:
    def __init__(self, template: dict):
        self.validate_template(template)
        self.template: dict = template

    def __call__(self, func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            try:
                request = None
                for arg in args:
                    if isinstance(arg, aiohttp.web_request.Request):
                        request = arg
                validated_data = {}
                if await request.read():
                    try:
                        validated_data = self.validate_data(await request.json(), self.template)
                    except WrongDataType as e:
                        raise ApiException(e, 400)
                result = await func(*args, validated_data=validated_data, **kwargs)
                return GoodResponse(result)
            except ApiException as e:
                return BadResponse(str(e), e.status)

        return wrap

    def validate_template(self, template):
        pass

    def validate_data(self, data, template, path=""):
        data = data.copy()
        validated_data = {}
        for key, template in template.items():
            is_required = key in data.get("__required__", [])
            try:
                if not data.get(key) and is_required:
                    raise DataMissing(f"{path}.{key}" if path else key)
                elif not data.get(key) and not is_required:
                    continue

                if isinstance(template, type):
                    validated_data[key] = template(data[key])
                elif isinstance(template, dict) and isinstance(data.get(key), dict):
                    validated_data[key] = self.validate_data(data[key], template,
                                                             f"{path}.{key}" if path else key)
                elif isinstance(template, list) and isinstance(data.get(key), list):

                    validated_data[key] = self.validate_list(data[key], template,
                                                             f"{path}.{key}" if path else key)
                else:
                    raise WrongDataType(f"{path}.{key}" if path else key)
            except ValueError:
                raise WrongDataType(f"{path}.{key}" if path else key)
        return validated_data

    def validate_list(self, data, template, path):
        template = template[0]
        validated_data = []
        if isinstance(template, type):
            for n, item in enumerate(data):
                try:
                    validated_data.append(template(item))
                except ValueError:
                    raise WrongDataType(f"{path}.{n}" if path else n)
        elif isinstance(template, dict):
            for n, item in enumerate(data):
                validated_data.append(self.validate_data(item, template,
                                                         f"{path}.{n}" if path else n))
        return validated_data
