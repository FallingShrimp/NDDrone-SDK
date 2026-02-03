import os
from typing import cast

import pyglet.window.win32 as pyglet
from psychopy import visual
from psychopy.visual.rect import Rect

from engine.api.parser.block import blockPosition, blockSize
from engine.util.position import topLeftToCenter
from engine.window.components import ProgressBar
from instances.config import config
from instances.loggers import loggerRenderer


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
        self.focus = -1
        self.progressBar = ProgressBar(self, (0, -100), (1000, 20))
        self.winHandle = cast(pyglet.Win32Window, self.winHandle)
        self.minimized = False

        @self.winHandle.event
        def on_hide():
            self.minimized = True

        @self.winHandle.event
        def on_show():
            self.minimized = False

        on_hide()
        on_show()

        def on_draw():
            if self.focus >= 0 and config.metadata:
                loggerRenderer.info(f"绘制聚焦框：{self.focus}")
                self.prompt(False)
                position = topLeftToCenter(
                    blockPosition(self.focus),
                    config.metadata["imageSize"],
                )
                size = blockSize(self.focus)
                position[0] += size[0] // 2
                position[1] -= size[1] // 2
                self.rect((position[0], position[1]), size, "red", 0.5)
                self.flip()
                self.focus = -1

        self.winHandle.on_draw = on_draw

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
        self.parsing()

    def parsing(self):
        self.coverText("正在解析用户意图...", True)

    def prompt(self, flip: bool = True):
        self.promptStim.draw()
        if flip:
            self.flip()

    def updateProgress(self, progress: float):
        self.progressBar.progress = progress
        self.progressBar.draw()

    def rect(
        self,
        pos: tuple[float, float],
        size: tuple[float, float],
        fill: str,
        opacity: float,
    ):
        stim = Rect(
            self,
            pos=pos,
            size=size,
            lineWidth=0,
            fillColor=fill,
            colorSpace="rgba",
            opacity=opacity,
        )
        stim.draw()
