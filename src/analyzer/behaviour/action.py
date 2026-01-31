from typing import Callable, Type
from analyzer.server import NeuroApiServer

store: dict[str, "BaseCommand"] = {}

CommandHandler = Callable[..., str | None]


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


def command(*args: ArgumentSlot):
    def decorator(func: CommandHandler):
        name = func.__name__
        store[name] = BaseCommand(name, args, func)
        return func

    return decorator


def cut(rawCommand: str) -> tuple[str, list[str]]:
    if ":" in rawCommand:
        main, args = rawCommand.split(":")
        args = args.split(",")
        return main, args
    else:
        return rawCommand, []


def parseArgs(rawArgs: list[str], template: tuple[ArgumentSlot, ...]):
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


def run(rawCommand: str, analyzer: NeuroApiServer) -> str | None:
    main, rawArgs = cut(rawCommand)
    base = store[main]
    realArgs = parseArgs(rawArgs, base.args)
    return base.handler(**(realArgs | {"analyzer": analyzer}))
