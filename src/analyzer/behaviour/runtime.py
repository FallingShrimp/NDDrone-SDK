from analyzer.behaviour.parser import parseCommand
from server import NeuroApiServer


def run(rawCommand: str, apiServer: NeuroApiServer) -> bytes | str | None:
    _main, args, base = parseCommand(rawCommand, "command")
    return base.handler(**(args | {"apiServer": apiServer}))
