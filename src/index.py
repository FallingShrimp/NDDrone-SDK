from analyzer.runner import NeuroApiRunner
from flymode import NDDroneFlymode
from analyzer import behaviour as NeuroApi
from engine.thread.ReceiveMessageThread import interpreter as ReceiveInterpreter

NeuroApi.init()
ReceiveInterpreter.init()

neuroApi = NeuroApiRunner()
neuroApi.start()
flymode = NDDroneFlymode()
flymode.init()
flymode.mainloop()
flymode.quit()
