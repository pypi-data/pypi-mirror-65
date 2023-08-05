from time import sleep
from typing import Callable

from slata_parser import TemporaryUnavailable


def safe_parsing(method: Callable):
    def wrapper(*args, safe=True, safe_attempts: int = 3, safe_interval: float = 5, **kwargs):
        attempts_amount = safe_attempts if safe else 1

        for attempt in range(attempts_amount):
            try:
                return method(*args, **kwargs)
            except TemporaryUnavailable:
                if attempt < attempts_amount - 1:
                    sleep(safe_interval)
        raise TemporaryUnavailable()

    return wrapper
