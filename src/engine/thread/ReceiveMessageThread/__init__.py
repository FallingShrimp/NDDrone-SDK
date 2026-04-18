import socket
import threading
import time

from analyzer.behaviour.parser import parseCommand
from engine.thread.SendMessageThread import SendMessageThread
from engine.util.network import checkConnection
from engine.window.simulation import SimulationWindow
from instances.loggers import loggerBehaviour


def run(
    rawCommand: str,
    thread: "ReceiveMessageThread",
    simulationWindow: SimulationWindow | None,
) -> bytes | str | None:
    _main, args, base = parseCommand(rawCommand, "receiveMessage")
    return base.handler(**(args | {"thread": thread, "simulation": simulationWindow}))


class ReceiveMessageThread(threading.Thread):
    def __init__(
        self,
        neuroApiSocket: socket.socket,
        drone: SendMessageThread,
        step: int,
    ):
        super().__init__()
        self.neuroApiSocket = neuroApiSocket
        self.drone = drone
        self.step = step
        self.isRunning = True
        self.stopEvent = threading.Event()
        self.simulationWindow: SimulationWindow | None = None
        self.pong = False

    def run(self) -> None:
        while not self.stopEvent.is_set():
            try:
                if checkConnection(self.neuroApiSocket):
                    data = self.neuroApiSocket.recv(1024)
                    if not data:
                        continue
                    message = data.decode("utf-8")
                    loggerBehaviour.info(f"收到消息：{message}")
                    run(message, self, self.simulationWindow)
            except OSError:
                self.stopEvent.set()
            time.sleep(0.1)
        loggerBehaviour.warning("已断开连接。")

    def close(self):
        self.stopEvent.set()
