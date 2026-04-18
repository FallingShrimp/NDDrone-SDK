import socket
import time
from datetime import datetime
from threading import Thread
from typing import Callable

from psychopy import core

from engine.util.network import checkConnection
from instances.loggers import loggerDrone


class SendMessageThread(Thread):
    _roboAddress: tuple[str, int]
    _sock: socket.socket
    _get_info_last_time = datetime.now()
    recb: Callable

    def __init__(self, roboAddress):
        super().__init__()
        self._roboAddress = roboAddress
        self._is_running = True
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("0.0.0.0", 1145))
        self.recb = lambda x: None

    def run(self):
        while self._is_running:
            try:
                if not self._is_running:
                    break
                response, ip = self._sock.recvfrom(128)
                response = response.decode(encoding="utf-8")
                loggerDrone.info("收到消息: " + response)
                self.recb(response)
                time.sleep(0.01)
            except Exception as e:
                if not self._is_running:
                    break
                loggerDrone.error(e)
                time.sleep(1)
        loggerDrone.warning("已断开连接。")

    def send(self, message: str):
        if checkConnection(self._sock):
            try:
                loggerDrone.info("发送消息: " + message)
                self._sock.sendto(message.encode(encoding="utf-8"), self._roboAddress)
            except Exception as e:
                loggerDrone.error("发送失败: " + str(e))
        else:
            loggerDrone.warning("未连接无人机，已跳过发送消息：" + message)

    def close(self):
        self._is_running = False
        core.wait(0.1)
        try:
            self._sock.close()
        except Exception:
            pass
