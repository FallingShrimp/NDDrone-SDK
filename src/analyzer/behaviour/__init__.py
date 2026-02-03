import random

from analyzer.behaviour.parser import ArgumentSlot, command
from analyzer.server import NeuroApiServer
from engine.thread.ReceiveMessageThread.interpreter import RSLT
from engine.util.network import checkConnection


@command(type="command")
def STOP(apiServer: NeuroApiServer):
    apiServer.running = False
    apiServer.quit()


@command(ArgumentSlot("timestamp", int), type="command")
def TIME(timestamp: int, apiServer: NeuroApiServer):
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
