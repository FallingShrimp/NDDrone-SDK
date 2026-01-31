from analyzer.behaviour.action import ArgumentSlot, command
from analyzer.server import NeuroApiServer
from engine.util.network import checkConnection


@command()
def STOP(apiServer: NeuroApiServer):
    apiServer.running = False
    apiServer.quit()


@command(ArgumentSlot("timestamp", int))
def TIME(timestamp: int, apiServer: NeuroApiServer):
    result = 0
    if checkConnection(apiServer.deviceThread.sock):
        epoch = apiServer.deviceThread.readFixedData(
            apiServer.config.winLEN + apiServer.config.lag,
            timestamp,
        )
        result = apiServer.analyzer.predict(epoch)[0]
    return f"RSLT:{result}"


def init():
    pass
