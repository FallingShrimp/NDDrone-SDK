from analyzer import behaviour as NeuroApiInterpreter
from analyzer.runner import NeuroApiRunner
from behaviour import handler as BehaviourHandler
from engine.thread.ReceiveMessageThread import interpreter as ReceiveInterpreter
from flymode import NDDroneFlymode

NeuroApiInterpreter.init()
ReceiveInterpreter.init()
BehaviourHandler.init()

neuroApi = NeuroApiRunner()
neuroApi.start()
flymode = NDDroneFlymode()
flymode.init()
flymode.mainloop()
flymode.quit()
