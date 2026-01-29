import os
import time

from psychopy import core, event

from engine.core.configCore import Config
from engine.thread.ReceiveMessageThread import ReceiveMessageThread
from engine.thread.SendMessageThread import SendMessageThread
from engine.util.connection import checkConnection, createClient
from engine.util.workdir import fromAssets
from engine.window.simulation import SimulationWindow
from loggers import loggerMain


class NDDroneFlymode:
    def __init__(self):
        self.config = Config()
        # 配置一些路径常量
        self.picturePath = fromAssets("frames")
        self.backgroundPath = fromAssets("background.jpg")
        self.promptPath = os.path.join(self.picturePath, "display_frame.png")
        # 主循环状态
        self.running = False
        # NeuroAPI接收数据
        self.neuroApiSocket = createClient(self.config.neuroApiAddress, 1)
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
        self.simulation = SimulationWindow(self.config.windowSize)

    def quit(self):
        self.stoploop()
        self.simulation.close()  # 关掉窗口
        self.messageReceiveThread.close()  # 先把接收线程关了，不然后面发STOP会报错
        if checkConnection(self.neuroApiSocket):
            self.neuroApiSocket.send(b"STOP\n")  # 关掉NeuroAPI
            self.neuroApiSocket.close()
        self.drone.send("land")  # 降落无人机防止耗电
        self.drone.close()
        loggerMain.info("Quitted.")
        loggerMain.info("Waiting for NeuroAPI to stop...")
        core.quit()

    def stoploop(self):  # 只是停止主循环，不会清理线程&刺激块窗口
        self.running = False

    def init(self):
        loggerMain.info("NDDrone-flymode initializing...")
        loggerMain.info("Starting drone...")
        self.drone.start()
        self.drone.send("command")
        time.sleep(1)
        self.drone.send("motoron")
        loggerMain.info("Loading frames...")
        self.simulation.coverText("Loading...", True)
        try:
            self.simulation.loadFlickerFrames(self.picturePath)
            self.simulation.loadDynamicFrames(self.backgroundPath, self.promptPath)
        except OSError:
            loggerMain.error("Frame files not found! Please generate before start.")
            self.quit()
        loggerMain.info("Simulation ready!")

    def mainloop(self):
        self.running = True
        self.messageReceiveThread.start()
        # 第一帧，先把提示帧展示出来，等按空格开始
        self.simulation.prompt()
        while self.running:
            try:
                keys = event.getKeys(keyList=["space", "escape"])
                if "escape" in keys:
                    self.stoploop()
                    break
                elif "space" in keys:
                    # 没连上就说明单纯调试刺激块屏幕，不管他即可
                    if checkConnection(self.neuroApiSocket):
                        # 给NeuroAI发消息准备开始接收识别结果
                        currentTime = int(time.time() * 1000)
                        self.neuroApiSocket.send(f"TIME:{currentTime}\n".encode("utf8"))
                    # 开始闪烁
                    self.simulation.flicker()
                core.wait(0.01)
            except Exception as e:
                loggerMain.error(e)
                self.stoploop()
                break
