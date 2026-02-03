from behaviour import handler as BehaviourHandler
from engine.thread.ReceiveMessageThread import interpreter as ReceiveInterpreter
from flymode import NDDroneFlymode


def main():
    ReceiveInterpreter.init()
    BehaviourHandler.init()
    flymode = NDDroneFlymode()
    flymode.init()
    flymode.mainloop()
    flymode.quit()


if __name__ == "__main__":
    main()
