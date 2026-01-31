from analyzer.behaviour.action import ArgumentSlot, command
from analyzer.server import AnalyzerServer


@command()
def STOP(analyzer: AnalyzerServer):
    analyzer.apiServer.running = False
    analyzer.apiServer.quit()


@command(ArgumentSlot("timestamp", int))
def TIME(timestamp: int, analyzer: AnalyzerServer):
    epoch = analyzer.apiServer.deviceThread.readFixedData(
        analyzer.apiServer.config.winLEN + analyzer.apiServer.config.lag,
        timestamp,
    )
    return analyzer.apiServer.analyzer.predict(epoch)[0]


def init():
    pass
