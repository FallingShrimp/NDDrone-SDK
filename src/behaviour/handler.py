from engine.api.behaviour.action import Forward
from engine.api.behaviour.handler import command


@command(0)
def command_0():
    return Forward(100)


def init():
    pass
