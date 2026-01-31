from analyzer.server import NeuroApiServer
from analyzer.behaviour.runtime import run
import threading


class NeuroApiRunner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = NeuroApiServer(self.parseCommand)

    def run(self):
        self.server.start()

    def parseCommand(self, message: str) -> str | None:
        return run(message, self.server)
