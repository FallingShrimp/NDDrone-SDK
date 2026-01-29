import queue
import threading
import time

from spatialFilter import FBCCA

from engine.core.configCore import Config
from engine.thread.NDThread import NDThread, loggerNeuroApi
from engine.util.connection import createServer, waitClient


class AnalyzerServer(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.apiServer = NeuroApiServer()

    def init(self):
        loggerNeuroApi.info("NeuroApi-server initializing...")
        self.apiServer.init()

    def run(self):
        self.apiServer.start()
        while self.apiServer.running:
            if self.apiServer.messageQueue.qsize() > 0:
                message = self.apiServer.messageQueue.get()
                if len(message) > 5:
                    stimulationTime = int(message[5:])
                    epoch = self.apiServer.deviceThread.readFixedData(
                        self.apiServer.config.winLEN + self.apiServer.config.lag,
                        stimulationTime,
                    )
                    result = self.apiServer.analyzer.predict(epoch)[0]
                    self.apiServer.clientSocket.send(f"RSLT:{result}".encode("utf-8"))
                time.sleep(0.01)

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

    def init(self):
        self.analyzer.fit()
        loggerNeuroApi.info("Waiting for client connection...")
        self.clientSocket, _address = waitClient(self.clientServer, 5)
        self.clientSocket.settimeout(20000)
        self.deviceThread.connect()

    def run(self):
        self.deviceThread.start()
        while True:
            consumeMsg = self.clientSocket.recv(1024)
            if consumeMsg:
                message = str(consumeMsg)[2:-1]
                self.messageQueue.put(message)
                event = message[0:4]
                if event == "STOP":
                    break
            time.sleep(0.1)
        self.running = False

    def quit(self):
        self.deviceThread.disconnect()
        self.clientServer.close()
        self.clientSocket.close()
