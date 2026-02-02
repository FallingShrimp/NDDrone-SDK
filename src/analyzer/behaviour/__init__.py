import random

from psychopy import event

from analyzer.behaviour.parser import ArgumentSlot, command
from analyzer.server import NeuroApiServer
from engine.thread.ReceiveMessageThread.interpreter import RSLT
from engine.util.network import checkConnection


@command(type="command")
def STOP(apiServer: NeuroApiServer):
    apiServer.running = False
    apiServer.quit()


@command(ArgumentSlot("timestamp", int), ArgumentSlot("useKey", bool), type="command")
def TIME(timestamp: int, useKey: bool, apiServer: NeuroApiServer):
    result = -1
    if checkConnection(apiServer.deviceThread.sock):
        epoch = apiServer.deviceThread.readFixedData(
            apiServer.config.winLEN + apiServer.config.lag,
            timestamp,
        )
        result = apiServer.analyzer.predict(epoch)[0]
    elif useKey:
        keys: list[str] = event.getKeys(keyList=list(range(9)))
        for key in keys:
            if key.isdigit():
                result = int(key)
                break
    else:
        result = random.randint(0, 8)
    return RSLT(result)


def init():
    pass
