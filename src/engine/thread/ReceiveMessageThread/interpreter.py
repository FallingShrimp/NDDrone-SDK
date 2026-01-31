from analyzer.behaviour.parser import command, ArgumentSlot
from engine.api.behaviour.handler import store
from engine.thread.ReceiveMessageThread import ReceiveMessageThread
from loggers import loggerBehaviour


@command(ArgumentSlot("result", int), type="receiveMessage")
def RSLT(result: int, thread: ReceiveMessageThread):
    loggerBehaviour.info(f"执行指令：{result}")
    if result in store:
        action = store[result]()
        thread.drone.send(str(action))
    else:
        loggerBehaviour.warning(f"指令{result}未注册处理程序。")


def init():
    pass
