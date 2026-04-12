import random

from analyzer.behaviour.parser import ArgumentSlot, command
from engine.util.network import checkConnection
from instances.loggers import loggerNeuroApi
from neuroApi import NeuroApiServer
from datetime import datetime


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
        dt = datetime.fromtimestamp(timestamp / 1000)
        if epoch is not None:
            result = apiServer.analyzer.predict(epoch)[0]
            with open(
                f"epoch/{dt.strftime('%Y-%m-%d_%H-%M-%S')}.txt",
                "w",
                encoding="utf8",
            ) as output:
                output.write(f"Result: {result}\n\n")
                for index in range(epoch.shape[0]):
                    output.write(
                        ",".join([str(x) for x in epoch[index, :].tolist()]) + "\n"
                    )
    else:
        loggerNeuroApi.warning("未连接ND8，采用随机数。")
        result = random.randint(0, 8)
    return RSLT(result)


def init():
    pass
