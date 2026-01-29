from typing import Callable

from engine.api.behaviour.action import DroneActionBase

BehaviourHandler = Callable[[], DroneActionBase]
