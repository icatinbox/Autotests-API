import json
import time
from json import JSONDecodeError
import allure
import requests
from core.http.retry import RetryConfig, should_retry


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
        self.retry_config = RetryConfig()

    def _request_once(self, path, method, attempt, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"

        # Сохраняем данные запроса в allure
        with allure.step(f'request {method.upper()} {path} | attempt {attempt}'):
            if "headers" in kwargs and kwargs["headers"]:
                _attach_json("request.headers", dict(kwargs["headers"]))
            if "params" in kwargs and kwargs["params"]:
                _attach_json("request.params", kwargs["params"])
            if "json" in kwargs and kwargs["json"] is not None:
                _attach_json("request.json", kwargs["json"])
            if "data" in kwargs and kwargs["data"]:
                _attach_text("request.data", str(kwargs["data"]))

        # Делаем запрос
        response = self.session.request(method, url, **kwargs)

        # Сохраняем данные ответа в allure
        _attach_text("response.status_code", str(response.status_code))
        _attach_json("response.headers", dict(response.headers))
        _attach_text("response.time_request", str(response.elapsed.total_seconds()))

        content_type = (response.headers.get("content-type") or "").lower()
        # Сохраняем json в allure, если content-type = application/json
        if "application/json" in content_type:
            try:
                _attach_json("response.json", response.json())
            except JSONDecodeError:
                _attach_text("response.body", response.text)
        else:
            _attach_text("response.body", response.text)

        return response

    def request(self, path, method, **kwargs):
        config = self.retry_config
        delay = config.delay
        last_exception = None
        last_response = None

        # kwargs.setdefault("timeout", 10)
        for attempt in range(1, config.attempts + 1):
            try:
                response = self._request_once(path, method, attempt, **kwargs)
                last_response = response

                if not should_retry(config=config, method=method, response=response):
                    return response

                if attempt < config.attempts:
                    with allure.step(f'retry {attempt} / response.status {response.status_code}'):
                        time.sleep(delay)
                    delay *= config.backoff
                    continue
                return response

            except Exception as e:
                last_exception = e

                with allure.step(f'retry {attempt} / {type(e).__name__}'):
                    _attach_text("exception", str(e))
                if not should_retry(config=config, method=method, response=last_response) or attempt == config.attempts:
                    raise

                with allure.step(f'"Retry after exception. Sleep {delay} sec"'):
                    time.sleep(delay)
                delay *= config.backoff

        if last_exception:
            raise last_exception
        return last_response


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