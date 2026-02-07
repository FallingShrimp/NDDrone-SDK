import random

from analyzer.behaviour.parser import ArgumentSlot, command
from engine.util.network import checkConnection
from instances.loggers import loggerNeuroApi
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
        if epoch is not None:
            data = epoch.tobytes()
            open(f"epoch/{timestamp}.txt", "wb").write(data)
            result = apiServer.analyzer.predict(epoch)[0]
    else:
        loggerNeuroApi.warning("未连接ND8，采用随机数。")
        result = random.randint(0, 8)
    return RSLT(result)


def init():
    pass
