import random
import zipfile
import os
from datetime import datetime

from analyzer.behaviour.parser import ArgumentSlot, command
from engine.api.timer.constants import TIME_FORMAT_FILE
from engine.util.network import checkConnection
from instances.loggers import loggerNeuroApi
from neuroApi import NeuroApiServer
from instances.config import config

BLOCK_ONE_TIME = 10
results: list[int] = []
for i in range(9):
    results.extend([i] * BLOCK_ONE_TIME)


@command(type="command")
def PING(**KW):
    from engine.thread.ReceiveMessageThread.interpreter import PONG

    return PONG()


@command(type="command")
def QUIT_SERVER(apiServer: NeuroApiServer):
    apiServer.running = False
    apiServer.quit()


@command(ArgumentSlot("timestamp", int), type="command")
def PREDICT_MIND(timestamp: int, apiServer: NeuroApiServer):
    from engine.thread.ReceiveMessageThread.interpreter import REACT_RESULT

    result = -1
    if checkConnection(apiServer.deviceThread.sock):
        epoch = apiServer.deviceThread.readFixedData(
            apiServer.config.winLEN + apiServer.config.lag,
            timestamp,
        )
        dt = datetime.fromtimestamp(timestamp / 1000)
        filedTime = dt.strftime(TIME_FORMAT_FILE)
        if epoch is not None and config.metadata is not None:
            result = apiServer.analyzer.predict(epoch)[0]
            targetResult = results[apiServer.predictedTimes]
            loggerNeuroApi.info(f"Mind result: {result}")
            loggerNeuroApi.info(
                f"Target result: {targetResult} [{','.join([str(x) for x in results])}]"
            )
            with open(
                f"epoch/{targetResult}-{result} {filedTime}.txt",
                "w",
                encoding="utf8",
            ) as output:
                output.write(f"Result: {result}\n\n")
                for index in range(epoch.shape[0]):
                    output.write(
                        ",".join([str(x) for x in epoch[index, :].tolist()]) + "\n"
                    )
        apiServer.predictedTimes += 1
        if apiServer.predictedTimes >= len(results):
            with zipfile.ZipFile(
                f"epochStore/{config.watcher} - {filedTime}.zip",
                "w",
            ) as f:
                for epochName in os.listdir("epoch"):
                    f.write(
                        f"epoch/{epochName}",
                        epochName.encode("utf8").decode("cp437"),
                    )
    else:
        loggerNeuroApi.warning("未连接ND8。")
        result = random.randint(0, 8)
    return REACT_RESULT(result)


def init():
    pass
