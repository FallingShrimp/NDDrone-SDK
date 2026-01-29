from analyzer.server import NeuroApiServer
from flymode import NDDroneFlymode

neuroApi = NeuroApiServer()
neuroApi.start()
flymode = NDDroneFlymode()
flymode.init()
flymode.mainloop()
flymode.quit()
