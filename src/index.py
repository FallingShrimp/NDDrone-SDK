import sys


def neuroApi():
    from analyzer import behaviour as NeuroApiInterpreter
    from analyzer.runner import NeuroApiRunner

    NeuroApiInterpreter.init()
    neuroApi = NeuroApiRunner()
    neuroApi.start()


def flymode():
    from behaviour import handler as BehaviourHandler
    from engine.thread.ReceiveMessageThread import interpreter as ReceiveInterpreter
    from flymode import NDDroneFlymode

    ReceiveInterpreter.init()
    BehaviourHandler.init()
    flymode = NDDroneFlymode()
    flymode.init()
    flymode.mainloop()
    flymode.quit()


if len(sys.argv) > 1:
    if sys.argv[1] == "neuroapi":
        neuroApi()
    elif sys.argv[1] == "flymode":
        flymode()
else:
    neuroApi()
    flymode()
