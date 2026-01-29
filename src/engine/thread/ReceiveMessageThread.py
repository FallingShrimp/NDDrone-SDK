import socket
import threading
import time

from engine.api.behaviour.handler import store
from engine.thread.SendMessageThread import SendMessageThread
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

    def run(self) -> None:
        while self.isRunning:
            consumeMsg = self.neuroApiSocket.recv(1024)
            if consumeMsg:
                message = str(consumeMsg)[2:-1]
                if len(message) > 5:
                    result = int(message[5:])
                    if result in store:
                        action = store[result]()
                        self.drone.send(str(action))
                    else:
                        loggerBehaviour.warning(
                            f"Handler not registered for result {result}."
                        )
            time.sleep(0.1)

    def close(self):
        self.isRunning = False
