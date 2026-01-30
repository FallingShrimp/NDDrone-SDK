import os
import pyglet.window.win32 as pyglet
from psychopy import visual
from typing import cast
from config import config
from engine.window.components import ProgressBar


class SimulationWindow(visual.Window):
    def __init__(self, size: tuple[int, int]):
        super().__init__(
            size,
            monitor="testMonitor",
            units="pix",
            fullscr=True,
            waitBlanking=True,
            color=(0, 0, 0),
            colorSpace="rgb255",
            screen=0,
            allowGUI=True,
        )
        self.progressBar = ProgressBar(self, (0, -100), (1000, 20))
        self.winHandle = cast(pyglet.Win32Window, self.winHandle)
        self.minimized = False

        @self.winHandle.event
        def on_hide():
            self.minimized = True

        @self.winHandle.event
        def on_show():
            self.minimized = False

    def coverText(self, text: str, draw: bool):
        stim = visual.TextStim(
            self,
            pos=[0, 0],
            text=text,
            color=(255, 255, 255),
            colorSpace="rgb255",
            bold=True,
        )
        if draw:
            stim.draw()
            self.flip()
        return stim

    def coverImage(self, imagePath: str, draw: bool):
        stim = visual.ImageStim(
            self,
            image=imagePath,
            pos=[0, 0],
            size=self.size,
            units="pix",
            flipVert=False,
        )
        if draw:
            stim.draw()
            self.flip()
        return stim

    def loadFlickerFrames(self, picturePath: str):
        result: list[visual.ImageStim] = []
        for frameIndex in range(config.frameCount):
            result.append(
                self.coverImage(
                    os.path.join(picturePath, f"{frameIndex}.png"),
                    False,
                )
            )
            self.updateProgress(frameIndex / config.frameCount)
            self.coverText(f"Loading frames {frameIndex}/{config.frameCount}...", True)
        self.flickerFrames = result
        return result

    def loadDynamicFrames(
        self,
        backgroundPath: str,
        promptPath: str,
    ):
        self.backgroundStim = self.coverImage(backgroundPath, False)
        self.promptStim = self.coverImage(promptPath, False)

    def flicker(self):
        for flickerFrame in self.flickerFrames:
            self.backgroundStim.draw()
            flickerFrame.draw()
            self.flip()
        self.prompt()

    def prompt(self):
        self.promptStim.draw()
        self.flip()

    def updateProgress(self, progress: float):
        self.progressBar.progress = progress
        self.progressBar.draw()
