import os
import time

from psychopy import core, event

from engine.core.configCore import Config
from engine.thread.ReceiveMessageThread import ReceiveMessaageThread
from engine.thread.SendMessageThread import SendMessageThread
from engine.util.connection import connectSocket, isConnected
from engine.util.workdir import fromAssets
from engine.window.monitor import MonitorWindow
from loggers import loggerMain


class NDDroneFlymode:
    def __init__(self):
        loggerMain.info("NDDrone-flymode initializing...")
        self.config = Config()
        # 配置一些路径常量
        self.picturePath = fromAssets("frames")
        self.backgroundPath = fromAssets("background.jpg")
        self.promptPath = os.path.join(self.picturePath, "display_frame.png")
        # 主循环状态
        self.running = False
        # NeuroAPI接收数据
        self.neuroApiSocket = connectSocket(self.config.neuroApiAddress, 1)
        self.neuroApiSocket.settimeout(20000)
        # 无人机发送指令
        self.drone = SendMessageThread(("192.168.10.1", 8889))
        # 无人机接收指令
        self.messageReceiver = ReceiveMessaageThread(self.neuroApiSocket, self.drone, 5)
        # 初始化闪烁窗口
        self.monitor = MonitorWindow(self.config.windowSize)

    def quit(self):
        self.stoploop()
        self.monitor.close()  # 关掉窗口
        self.neuroApiSocket.send(b"STOP")  # 关掉NeuroAPI
        self.neuroApiSocket.close()
        self.drone.send("land")  # 降落无人机防止耗电
        self.drone.close()
        self.drone.join()
        self.messageReceiver.close()  # 关掉接收线程
        self.messageReceiver.join()
        core.quit()  # 退出

    def stoploop(self):  # 只是停止主循环，不会清理线程&刺激块窗口
        self.running = False

    def init(self):
        loggerMain.info("Starting drone...")
        self.drone.start()
        self.drone.send("command")
        time.sleep(1)
        self.drone.send("motoron")
        loggerMain.info("Loading frames...")
        self.monitor.coverText("Loading...", True)
        self.monitor.loadFlickerFrames(self.picturePath)
        self.monitor.loadDynamicFrames(self.backgroundPath, self.promptPath)

    def mainloop(self):
        self.running = True
        self.messageReceiver.start()
        # 第一帧，先把提示帧展示出来，等按空格开始
        self.monitor.prompt()
        while self.running:
            event.waitKeys(keyList=["space"])
            if isConnected(self.neuroApiSocket):
                # 给NeuroAI发消息准备开始接收识别结果
                currentTime = int(time.time() * 1000)
                self.neuroApiSocket.send(f"TIME:{currentTime}".encode("utf8"))
            # 开始闪烁
            self.monitor.flicker()
            # 闪烁完了，等按空格继续
            while True:
                try:
                    keys = event.getKeys()
                    if "escape" in keys:
                        self.stoploop()
                        break
                    elif "space" in keys:
                        break
                    # （软件计时器不精确，1帧可能不够休息）
                    time.sleep(2 / 60)
                except Exception as e:
                    loggerMain.error(e)
                    self.stoploop()
                    break
