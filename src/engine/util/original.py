from typing import Any, Callable


def retry(
    maxTimes: int,
) -> Callable[[Callable[[], object | bool]], Callable[[], tuple[Any, bool]]]:
    def decorator(func):
        def wrapper():
            times = 0
            while times < maxTimes:
                result = func()
                if result is not False:
                    return result, True
                else:
                    times += 1
            return None, False

        return wrapper

    return decorator


def waitKeyboardError() -> None:
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


def readKeyByValue(data: dict, value: Any):
    for key, val in data.items():
        if val == value:
            return key
    return None
