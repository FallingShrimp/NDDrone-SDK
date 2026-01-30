from psychopy import visual
from psychopy.visual.rect import Rect


class ProgressBar:
    def __init__(
        self,
        window: visual.Window,
        position: tuple[float, float],
        size: tuple[float, float],
    ):
        self.window = window
        self.position = position
        self.size = size
        self.progress = 0.0
        self.bar = Rect(
            self.window,
            pos=self.position,
            size=self.size,
            fillColor="gray",
        )
        self.fill = Rect(
            self.window,
            pos=self.position,
            size=(self.size[0] * self.progress, self.size[1]),
            fillColor="white",
        )

    def draw(self):
        self.fill.size = (self.size[0] * self.progress, self.size[1])
        self.fill.pos[0] = (self.size[0] - self.fill.size[0]) / -2
        self.bar.draw()
        self.fill.draw()
