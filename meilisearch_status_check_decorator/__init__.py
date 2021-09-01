from __future__ import annotations

from functools import wraps
from time import sleep
from typing import Any, Callable

from meilisearch.errors import MeiliSearchApiError
from meilisearch.index import Index


def status_check(index: Index) -> Callable:
    def decorator_status_check(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                initial_status_count = len(index.get_all_update_status())
            except MeiliSearchApiError:
                initial_status_count = 0

            result = func(*args, **kwargs)

            errors = False
            all_status = index.get_all_update_status()

            while True:
                if not [
                    x["status"] for x in all_status if x["status"] not in ["processed", "failed"]
                ]:
                    break

                sleep(1)
                all_status = index.get_all_update_status()

            if len(all_status) == initial_status_count + 1:
                status = all_status[-1:]
                if status[0]["status"] == "failed":
                    errors = True
            else:
                status = all_status[initial_status_count:]
                for s in status:
                    if s["status"] == "failed":
                        errors = True

            if errors:
                print(f"FAILED: {status}")  # noqa: T001

            return result

        return wrapper

    return decorator_status_check
