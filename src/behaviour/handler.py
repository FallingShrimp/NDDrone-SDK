from engine.api.behaviour.action import (
    Down,
    Forward,
    Land,
    Right,
    Takeoff,
    Up,
    Left,
    Backward,
    Flip,
)
from engine.api.behaviour.handler import command

STEP_DISTANCE = 50

"""
export const outputResultMap: Record<string, number> = {
    "up": 1,
    "down": 3,
    "left": 7,
    "right": 5,
    "forward": 4,
    "back": 6,
    "takeoff": 0,
    "land": 2,
    "flip": 8,
};"""


@command(0)
def zero():
    return Takeoff()


@command(1)
def one():
    return Up(STEP_DISTANCE)


@command(2)
def two():
    return Land()


@command(3)
def three():
    return Down(STEP_DISTANCE)


@command(4)
def four():
    return Forward(STEP_DISTANCE)


@command(5)
def five():
    return Right(STEP_DISTANCE)


@command(6)
def six():
    return Backward(STEP_DISTANCE)


@command(7)
def seven():
    return Left(STEP_DISTANCE)


@command(8)
def eight():
    return Flip("l")


def init():
    pass
