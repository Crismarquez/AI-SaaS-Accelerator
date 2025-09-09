from typing import Callable, TypeVar
import time


T = TypeVar("T")


def retry(times: int = 3, delay_seconds: float = 0.2):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last_exc = exc
                    time.sleep(delay_seconds)
            if last_exc:
                raise last_exc
        return wrapper
    return decorator


