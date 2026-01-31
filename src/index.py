from analyzer.runner import NeuroApiRunner
from flymode import NDDroneFlymode
from analyzer import behaviour as NeuroApiInterpreter
from engine.thread.ReceiveMessageThread import interpreter as ReceiveInterpreter

NeuroApiInterpreter.init()
ReceiveInterpreter.init()

neuroApi = NeuroApiRunner()
neuroApi.start()
flymode = NDDroneFlymode()
flymode.init()
flymode.mainloop()
flymode.quit()
