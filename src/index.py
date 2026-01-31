from analyzer.runner import NeuroApiRunner
from flymode import NDDroneFlymode

neuroApi = NeuroApiRunner()
neuroApi.start()
flymode = NDDroneFlymode()
flymode.init()
flymode.mainloop()
flymode.quit()
