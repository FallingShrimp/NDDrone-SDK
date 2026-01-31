from analyzer.server import AnalyzerServer
from analyzer.behaviour import init, action

init()


class NeuroApiRunner:
    def __init__(self) -> None:
        self.server = AnalyzerServer(self.parseCommand)

    def start(self):
        self.server.start()

    def parseCommand(self, message: str) -> str | None:
        return action.run(message, self.server)
