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
import random

STEP_DISTANCE = 50
SMALLER = 0.75


@command(0)
def zero():
    return Takeoff()


@command(1)
def one():
    return Up(STEP_DISTANCE * SMALLER)


@command(2)
def two():
    return Land()


@command(3)
def three():
    return Down(STEP_DISTANCE * SMALLER)


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
    return Flip(random.choice(["l", "r"]))


def init():
    pass
