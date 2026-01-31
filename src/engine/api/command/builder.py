from typing import Any


def buildCommand(main: str, args: list[Any]) -> str:
    result = f"{main}"
    if len(args) > 0:
        result += f":{','.join([str(arg) for arg in args])}"
    return result
