from dataclasses import dataclass

import requests

@dataclass(frozen=True)
class RetryConfig:
    attempts: int = 3
    delay: float = 1.0
    backoff: float = 2.0
    retry_statuses: tuple[int] = (408, 429, 500, 502, 503, 504)
    retry_methods: tuple[str] = ("GET", "HEAD", "OPTIONS", "PUT", "DELETE")
    retry_on_exceptions: tuple[type[Exception]] = (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
    )

def should_retry(config: RetryConfig, method: str, response=None, exception:Exception | None = None):
    method_upper = method.upper()

    if method_upper not in config.retry_methods:
        return False

    if exception is not None:
        return isinstance(exception, config.retry_on_exceptions)

    if response is not None:
        return response.status_code in config.retry_statuses

    return False