from pydantic import BaseModel


class DroneActionBase(BaseModel):
    command: str
    args: list

    def __init__(self, command: str, args: list):
        super().__init__(command=command, args=args)

    def __str__(self) -> str:
        return f"{self.command} {' '.join([str(round(arg) if isinstance(arg, (int, float)) else arg) for arg in self.args])}".strip()


class Forward(DroneActionBase):
    def __init__(self, distance: float):
        super().__init__(command="forward", args=[distance])


class Backward(DroneActionBase):
    def __init__(self, distance: float):
        super().__init__(command="back", args=[distance])


class Left(DroneActionBase):
    def __init__(self, distance: float):
        super().__init__(command="left", args=[distance])


class Right(DroneActionBase):
    def __init__(self, distance: float):
        super().__init__(command="right", args=[distance])


class Up(DroneActionBase):
    def __init__(self, distance: float):
        super().__init__(command="up", args=[distance])


class Down(DroneActionBase):
    def __init__(self, distance: float):
        super().__init__(command="down", args=[distance])


class Takeoff(DroneActionBase):
    def __init__(self):
        super().__init__(command="takeoff", args=[])


class Land(DroneActionBase):
    def __init__(self):
        super().__init__(command="land", args=[])


class Translate(DroneActionBase):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(command="go", args=[x, y, z])


class Flip(DroneActionBase):
    def __init__(self, direction: str):
        super().__init__(command="flip", args=[direction])
