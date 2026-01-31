import socket
import threading
import time

from engine.api.behaviour.handler import store
from engine.thread.SendMessageThread import SendMessageThread
from engine.util.network import checkConnection
from loggers import loggerBehaviour


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
    ) -> None:
        super().__init__()
        self.neuroApiSocket = neuroApiSocket
        self.drone = drone
        self.step = step
        self.isRunning = True
        self.stop_event = threading.Event()

    def run(self) -> None:
        while not self.stop_event.is_set():
            try:
                if checkConnection(self.neuroApiSocket):
                    data = self.neuroApiSocket.recv(1024)
                    if not data:
                        continue
                    message = data.decode("utf-8")
                    if len(message) > 5:
                        result = int(message[5:])
                        if result in store:
                            action = store[result]()
                            self.drone.send(str(action))
                        else:
                            loggerBehaviour.warning(f"指令{result}未注册处理程序。")
            except OSError:
                self.stop_event.set()
            time.sleep(0.01)
        loggerBehaviour.warning("已断开连接。")

    def close(self):
        self.stop_event.set()
