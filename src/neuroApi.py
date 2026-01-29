from analyzer.server import AnalyzerServer
from engine.util.original import waitKeyboardError

server = AnalyzerServer()
server.init()
server.start()
waitKeyboardError()
server.quit()
