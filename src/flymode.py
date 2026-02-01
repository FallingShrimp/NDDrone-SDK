import os
import time
import warnings
from engine.api.command.builder import buildCommand
import state
import keyboard
import pyglet.gl.lib

from psychopy import core, event, logging

from engine.thread.ReceiveMessageThread import ReceiveMessageThread
from engine.thread.SendMessageThread import SendMessageThread
from engine.util.network import checkConnection, createClient
from engine.util.workdir import fromAssets
from engine.window.simulation import SimulationWindow
from loggers import loggerMain
from config import config

logging.console.setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")


class NDDroneFlymode:
    def __init__(self):
        # 配置一些路径常量
        self.picturePath = fromAssets("frames")
        self.backgroundPath = fromAssets("background.jpg")
        self.promptPath = os.path.join(self.picturePath, "display_frame.png")
        # 主循环状态
        self.running = False
        # NeuroAPI接收数据
        self.neuroApiSocket = createClient(config.neuroApiAddress, 1)
        self.neuroApiSocket.settimeout(20000)
        # 无人机发送指令
        self.drone = SendMessageThread(("192.168.10.1", 8889))
        # 无人机接收指令
        self.messageReceiveThread = ReceiveMessageThread(
            self.neuroApiSocket,
            self.drone,
            50,
        )
        # 初始化闪烁窗口
        self.simulation = SimulationWindow(config.windowSize)
        keyboard.add_hotkey("m", self.toggleSimulation)

    def toggleSimulation(self):
        try:
            if self.simulation.minimized:
                self.simulation.winHandle.maximize()
                self.simulation.winHandle.activate()
                loggerMain.info("窗口已最大化")
            else:
                self.simulation.winHandle.minimize()
                loggerMain.info("窗口已最小化")
        except pyglet.gl.lib.GLException:
            self.simulation.minimized = not self.simulation.minimized
            self.toggleSimulation()

    def quit(self):
        self.stoploop()
        self.simulation.close()  # 关掉窗口
        self.messageReceiveThread.close()  # 先把接收线程关了，不然后面发STOP会报错
        if checkConnection(self.neuroApiSocket):
            self.neuroApiSocket.send(buildCommand("STOP", [], True))  # 关掉NeuroAPI
            self.neuroApiSocket.close()
        self.drone.send("land")  # 降落无人机防止耗电
        self.drone.close()
        loggerMain.info("已退出。")
        state.flymode = False
        state.prompt()

    def stoploop(self):  # 只是停止主循环，不会清理线程&刺激块窗口
        self.running = False

    def init(self):
        loggerMain.info("NDDrone-flymode 正在初始化...")
        loggerMain.info("正在启动无人机...")
        self.drone.start()
        self.drone.send("command")
        time.sleep(1)
        self.drone.send("motoron")
        loggerMain.info("正在加载逐帧图...")
        try:
            self.simulation.loadFlickerFrames(self.picturePath)
            self.simulation.loadDynamicFrames(self.backgroundPath, self.promptPath)
        except OSError:
            loggerMain.error("未找到帧文件！请先运行生成命令。")
            self.quit()
        loggerMain.info("闪烁窗口已就绪！")

    def mainloop(self):
        self.running = True
        self.messageReceiveThread.start()
        # 第一帧，先把提示帧展示出来，等按空格开始
        self.simulation.prompt()
        while self.running:
            try:
                keys = event.getKeys(keyList=["space", "escape"])
                if "escape" in keys:
                    loggerMain.info("正在退出")
                    self.stoploop()
                    break
                elif "space" in keys:
                    loggerMain.info("正在闪烁")
                    # 没连上就说明单纯调试刺激块屏幕，不管他即可
                    if checkConnection(self.neuroApiSocket):
                        # 给NeuroAPI发消息准备开始接收识别结果
                        currentTime = int(time.time() * 1000)
                        self.neuroApiSocket.send(
                            buildCommand("TIME", [currentTime], True)
                        )
                    # 开始闪烁
                    self.simulation.flicker()
                core.wait(0.01)
            except Exception as e:
                loggerMain.error(e)
                self.stoploop()
                break
