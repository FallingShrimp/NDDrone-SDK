from typing import Any, Callable, Literal, Type

from engine.api.command.builder import buildCommand

sendStore: dict[str, "BaseCommand"] = {}
receiveStore: dict[str, "BaseCommand"] = {}

CommandHandler = Callable[..., bytes | str | None]
ParserType = Literal["command"] | Literal["receiveMessage"]


class ArgumentSlot:
    type: Type
    name: str

    def __init__(self, name: str, type: Type) -> None:
        self.type = type
        self.name = name


class BaseCommand:
    main: str
    args: tuple[ArgumentSlot, ...]
    handler: CommandHandler

    def __init__(
        self, main: str, args: tuple[ArgumentSlot, ...], handler: CommandHandler
    ) -> None:
        self.main = main
        self.args = args
        self.handler = handler


def getStore(type: ParserType):
    return sendStore if type == "command" else receiveStore


def command(
    *args: ArgumentSlot,
    type: ParserType,
) -> Callable[[CommandHandler], Callable[..., bytes]]:
    def decorator(func: CommandHandler):
        name = func.__name__
        getStore(type)[name] = BaseCommand(name, args, func)

        def wrapper(*args):
            return buildCommand(name, list(args), type == "command")

        return wrapper

    return decorator


def cut(rawCommand: str) -> tuple[str, list[str]]:
    if ":" in rawCommand:
        main, args = rawCommand.split(":")
        args = args.split(",")
        return main, args
    else:
        return rawCommand, []


def parseArgs(rawArgs: list[str], template: tuple[ArgumentSlot, ...]) -> dict[str, Any]:
    if len(rawArgs) != len(template):
        raise ValueError("参数不匹配！")
    result = {}
    for i in range(len(template)):
        slot = template[i]
        data = rawArgs[i]
        try:
            result[slot.name] = slot.type(data)
        except Exception as e:
            raise ValueError(f"参数类型无效：{e}")
    return result


def parseCommand(
    rawCommand: str, type: ParserType
) -> tuple[str, dict[str, Any], BaseCommand]:
    main, rawArgs = cut(rawCommand)
    base = getStore(type)[main]
    realArgs = parseArgs(rawArgs, base.args)
    return main, realArgs, base
