import queue
import threading
import time
from typing import Callable

from analyzer.spatialFilter import FBCCA
from engine.core.configCore import Config
from engine.thread.NDThread import NDThread
from engine.util.network import checkConnection, createServer, waitClient
from instances import state
from instances.loggers import loggerNeuroApi


class AnalyzerServer(threading.Thread):
    def __init__(
        self,
        parseCommand: Callable[[str], bytes | str | None],
        apiServer: "NeuroApiServer",
    ) -> None:
        super().__init__()
        self.parseCommand = parseCommand
        self.apiServer = apiServer

    def run(self):
        while self.apiServer.running:
            # try:
            if (
                hasattr(self.apiServer, "clientSocket")
                and checkConnection(self.apiServer.clientSocket)
                and self.apiServer.messageQueue.qsize() > 0
            ):
                message = self.apiServer.messageQueue.get()
                loggerNeuroApi.info(f"处理消息: [bold]{message}[/bold]")
                result = self.parseCommand(message)
                if result:
                    if isinstance(result, bytes):
                        result = result.decode("utf8")
                    loggerNeuroApi.info(f"发送消息: [bold]{result}[/bold]")
                    if isinstance(result, str):
                        self.apiServer.clientSocket.send(result.encode("utf8"))
            time.sleep(0.01)
        # except Exception as e:
        #     loggerNeuroApi.error(e)
        #     time.sleep(0.01)


class NeuroApiServer(threading.Thread):
    def __init__(self, parseCommand: Callable[[str], bytes | str | None]):
        super().__init__()
        self.config = Config()
        self.messageQueue = queue.Queue(0)
        self.clientServer = createServer(("", self.config.neuroApiAddress[1]))
        self.analyzer = FBCCA(
            srate=self.config.srate,
            frequency=self.config.frequency,
            winLEN=self.config.winLEN,
        )
        self.deviceThread = NDThread(
            deviceAddress=self.config.deviceAddress,
            srate=self.config.srate,
            record_srate=self.config.record_srate,
        )
        self.running = True
        self.analyzerThread = AnalyzerServer(parseCommand, self)

    def run(self):
        self.analyzerThread.start()
        self.analyzer.fit()
        self.clientSocket, _address = waitClient(self.clientServer, 5)
        self.clientSocket.settimeout(20000)
        self.deviceThread.connect()
        self.deviceThread.start()
        while self.running:
            try:
                consumeMsg = self.clientSocket.recv(1024)
                if consumeMsg:
                    messages = consumeMsg.decode("utf8").split("\n")
                    messages.remove("")
                    for message in messages:
                        loggerNeuroApi.info(
                            f"[white]收到消息: [bold]{message}[/bold][/white]"
                        )
                        self.messageQueue.put(message)
                time.sleep(0.1)
            except Exception as e:
                print(1)
                loggerNeuroApi.error(e)
        self.running = False

    def quit(self):
        self.deviceThread.disconnect()
        self.clientServer.close()
        self.clientSocket.close()
        loggerNeuroApi.info("服务器已关闭。")
        state.neuroapi = False
        state.prompt()
