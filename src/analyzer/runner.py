from analyzer.server import NeuroApiServer
from analyzer.behaviour import init, action
import threading

init()


class NeuroApiRunner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = NeuroApiServer(self.parseCommand)

    def run(self):
        self.server.start()

    def parseCommand(self, message: str) -> str | None:
        return action.run(message, self.server)
