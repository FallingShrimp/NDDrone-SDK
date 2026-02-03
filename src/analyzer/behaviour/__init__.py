import random

from analyzer.behaviour.parser import ArgumentSlot, command
from engine.util.network import checkConnection
from neuroApi import NeuroApiServer


@command(type="command")
def STOP(apiServer: NeuroApiServer):
    apiServer.running = False
    apiServer.quit()


@command(ArgumentSlot("timestamp", int), type="command")
def TIME(timestamp: int, apiServer: NeuroApiServer):
    from engine.thread.ReceiveMessageThread.interpreter import RSLT

    result = -1
    if checkConnection(apiServer.deviceThread.sock):
        epoch = apiServer.deviceThread.readFixedData(
            apiServer.config.winLEN + apiServer.config.lag,
            timestamp,
        )
        result = apiServer.analyzer.predict(epoch)[0]
    else:
        result = random.randint(0, 8)
    return RSLT(result)


def init():
    pass
