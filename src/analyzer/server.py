import queue
import threading
import time
from typing import Callable
import state

from analyzer.spatialFilter import FBCCA
from engine.core.configCore import Config
from engine.thread.NDThread import NDThread, loggerNeuroApi
from engine.util.connection import createServer, waitClient


class AnalyzerServer(threading.Thread):
    def __init__(self, commandParser: Callable[[str], str | None]) -> None:
        super().__init__()
        self.apiServer = NeuroApiServer()
        self.commandParser = commandParser

    def run(self):
        self.apiServer.start()
        while self.apiServer.running:
            try:
                if self.apiServer.messageQueue.qsize() > 0:
                    message = self.apiServer.messageQueue.get()
                    result = self.commandParser(message)
                    if result:
                        self.apiServer.clientSocket.send(result.encode("utf8"))
                    time.sleep(0.01)
            except Exception as e:
                loggerNeuroApi.error(e)
                self.apiServer.running = False
        self.quit()

    def quit(self):
        self.apiServer.quit()


class NeuroApiServer(threading.Thread):
    def __init__(self):
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

    def run(self):
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
                time.sleep(0.01)
            except Exception as e:
                loggerNeuroApi.error(e)
        self.running = False

    def quit(self):
        self.deviceThread.disconnect()
        self.clientServer.close()
        self.clientSocket.close()
        loggerNeuroApi.info("服务器已关闭。")
        state.neuroapi = False
        state.prompt()
