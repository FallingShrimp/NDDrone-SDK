from analyzer.behaviour.parser import command, ArgumentSlot, parseCommand
from engine.api.behaviour.handler import store
from engine.thread.ReceiveMessageThread import ReceiveMessageThread
from loggers import loggerBehaviour


@command(ArgumentSlot("result", int), type="receiveMessage")
def RSLT(result: int, thread: ReceiveMessageThread):
    if result in store:
        action = store[result]()
        thread.drone.send(str(action))
    else:
        loggerBehaviour.warning(f"指令{result}未注册处理程序。")


def run(rawCommand: str, thread: ReceiveMessageThread) -> str | None:
    _main, args, base = parseCommand(rawCommand, "receiveMessage")
    return base.handler(**(args | {"thread": thread}))
