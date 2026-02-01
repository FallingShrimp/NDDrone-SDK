import socket
import threading
import time

from engine.thread.SendMessageThread import SendMessageThread
from engine.util.network import checkConnection
from engine.window.simulation import SimulationWindow
from loggers import loggerBehaviour
from analyzer.behaviour.parser import parseCommand


def run(
    rawCommand: str, thread: "ReceiveMessageThread", simulationWindow: SimulationWindow
) -> bytes | str | None:
    _main, args, base = parseCommand(rawCommand, "receiveMessage")
    return base.handler(**(args | {"thread": thread, "simulation": simulationWindow}))


class ReceiveMessageThread(threading.Thread):
    neuroApiSocket: socket.socket
    drone: SendMessageThread
    step: int
    isRunning: bool

    def __init__(
        self,
        neuroApiSocket: socket.socket,
        drone: SendMessageThread,
        step: int,
        simulationWindow: SimulationWindow,
    ):
        super().__init__()
        self.neuroApiSocket = neuroApiSocket
        self.drone = drone
        self.step = step
        self.isRunning = True
        self.stopEvent = threading.Event()
        self.simulationWindow = simulationWindow

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
            time.sleep(0.01)
        loggerBehaviour.warning("已断开连接。")

    def close(self):
        self.stopEvent.set()
