import json
from json import JSONDecodeError
import allure
import requests

def _attach_json(name: str, data):
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )

def _attach_text(name: str, text: str):
    allure.attach(text or "", name=name, attachment_type=allure.attachment_type.TEXT)

class ClientApi:
    def __init__(self, base_url, verify=True):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update({'accept': 'application/json'})

    def request(self, path, method, **kwargs):
        # Сохраняем данные запроса в allure
        with allure.step(f'request {method.upper()} {path}'):
            if "headers" in kwargs and kwargs["headers"]:
                _attach_json("request.headers", dict(kwargs["headers"]))
            if "params" in kwargs and kwargs["params"]:
                _attach_json("request.params", kwargs["params"])
            if "json" in kwargs and kwargs["json"] is not None:
                _attach_json("request.json", kwargs["json"])
            if "data" in kwargs and kwargs["data"]:
                _attach_text("request.data", str(kwargs["data"]))

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)

        # Сохраняем данные ответа в allure
        _attach_text("response.status_code", str(response.status_code))
        _attach_json("response.headers", dict(response.headers))
        _attach_text("response.time_request", str(response.elapsed.total_seconds()))

        content_type = response.headers.get('content-type').lower() if response.headers.get('content-type') else []

            # Сохраняем json в allure, если content-type = application/json
        if "application/json" in content_type:
            try:
                _attach_json("response.json", response.json())
            except JSONDecodeError:
                _attach_text("response.body", response.text)
        else:
            _attach_text("response.body", response.text)

        return response

    def request_json(self, path, method, is_raise=True, **kwargs):
        response = self.request(path, method, **kwargs)
        if is_raise:
            response.raise_for_status()
        try:
            data = response.json()
        except JSONDecodeError as e:
            return response, f'json is not find {e}'
        else:
            return response, data

    def request_auth(self, payload):
        path = '/api/Accounts/LogInWithRedirect'
        response = self.request(path=path, method='POST', json=payload)
        response.raise_for_status()