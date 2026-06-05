import os
import shutil
import time
import warnings

import keyboard
import pyglet.gl.lib
from psychopy import event, logging

from analyzer.behaviour import PING, QUIT_SERVER, PREDICT_MIND
from engine.thread.ReceiveMessageThread import ReceiveMessageThread
from engine.thread.SendMessageThread import SendMessageThread
from engine.util.network import checkConnection, createClient
from engine.util.workdir import fromAssets
from engine.window.simulation import SimulationWindow
from instances import state
from instances.config import config
from instances.loggers import loggerMain

logging.console.setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")


class NDDroneFlymode:
    def __init__(self):
        if config.metadata is None:
            raise Exception("未找到刺激块元数据！请先编译刺激块。")
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
        self.drone = SendMessageThread(config.droneIp)
        # 无人机接收指令
        self.messageReceiveThread = ReceiveMessageThread(
            self.neuroApiSocket,
            self.drone,
            50,
        )

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
            self.neuroApiSocket.send(QUIT_SERVER())  # 关掉NeuroAPI
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
        loggerMain.info("正在初始化epoches")
        shutil.rmtree("epoch")
        os.makedirs("epoch", exist_ok=True)

    def mainloop(self):
        loggerMain.info("正在首次握手NeuroAPI...")
        self.messageReceiveThread.start()
        self.neuroApiSocket.send(PING())
        while not self.messageReceiveThread.pong:
            pass
        loggerMain.info("NeuroAPI首次握手完成。")
        loggerMain.info("正在初始化刺激块窗口...")
        self.simulation = SimulationWindow(config.windowSize)
        keyboard.add_hotkey("m", self.toggleSimulation)
        loggerMain.info("正在加载逐帧图...")
        try:
            self.simulation.loadFlickerFrames(self.picturePath)
            self.simulation.loadDynamicFrames(self.backgroundPath, self.promptPath)
        except OSError:
            loggerMain.error("未找到闪烁帧资源！请先编译刺激块。")
            self.quit()
        self.messageReceiveThread.simulationWindow = self.simulation
        loggerMain.info("闪烁窗口已就绪。")
        self.running = True
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
                        self.neuroApiSocket.send(PREDICT_MIND(currentTime))
                    # 开始闪烁
                    self.simulation.simulate()
                time.sleep(0.01)
                self.simulation.winHandle.on_draw()
            except Exception as e:
                loggerMain.error(e)
                self.stoploop()
                break
