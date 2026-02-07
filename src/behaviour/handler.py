from engine.api.behaviour.action import Land, Takeoff
from engine.api.behaviour.handler import command


@command(0)
def command_0():
    return Takeoff()


@command(3)
def landw():
    return Land()


def init():
    pass
