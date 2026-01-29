import socket
import threading
import time
from typing import Callable

from engine.api.behaviour.handler import store
from engine.thread.RoboMasterThread import RoboMasterThread
from loggers import loggerBehaviour


class ReceiveMessaageThread(threading.Thread):
    neuroApiSocket: socket.socket
    drone: RoboMasterThread
    step: int
    stopFlag: Callable[..., bool]

    def __init__(
        self,
        neuroApiSocket: socket.socket,
        drone: RoboMasterThread,
        step: int,
        stopFlag: Callable[..., bool],
    ) -> None:
        super().__init__()
        self.neuroApiSocket = neuroApiSocket
        self.drone = drone
        self.step = step
        self.stopFlag = stopFlag

    def run(self) -> None:
        while self.isRunning():
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

    def isRunning(self):
        return not self.stopFlag()
