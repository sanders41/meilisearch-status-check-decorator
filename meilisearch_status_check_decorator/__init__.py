from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from meilisearch.index import Index


def status_check(index: Index) -> Callable:
    def decorator_status_check(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            all_status = index.get_all_update_status()
            last_status = all_status.pop()
            if last_status["status"] == "failed":
                print(f"FAILED: {last_status}")  # noqa: T001

            return result

        return wrapper

    return decorator_status_check
