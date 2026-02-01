from typing import Any


def buildCommand(main: str, args: list[Any], separator: bool = False) -> bytes:
    result = f"{main}"
    if len(args) > 0:
        result += f":{','.join([str(arg) for arg in args])}"
    if separator:
        result += "\n"
    return result.encode("utf8")
