import json
import numpy as np
from configparser import ConfigParser


class Config:
    def __init__(self) -> None:
        self.defaultConfig()

    def defaultConfig(
        self,
    ):
        self.displayINFO()
        self.expINFO()
        self.connectINFO()
        self.externalINFO()
        self.metadataINFO()

    def displayINFO(self, refreshRate=60, window_size=(1920, 1080)):
        self.refreshRate = refreshRate
        self.windowSize = window_size

    def expINFO(
        self,
        srate=250,
        recordRate=1000,
        winLEN=3,
        lag=0.14,
        frequency=np.arange(8, 17, 1),
    ):
        self.srate = srate
        self.record_srate = recordRate
        self.winLEN = winLEN
        self.lag = lag
        self.frequency = frequency

    def connectINFO(
        self,
        droneAddress=("192.168.10.1", 8889),
        deviceAddress=("127.0.0.1", 8899),
        neuroApiAddress=("127.0.0.1", 11000),
    ):
        self.roboAddress = droneAddress
        self.deviceAddress = deviceAddress
        self.neuroApiAddress = neuroApiAddress

    def externalINFO(self):
        cf = ConfigParser()
        cf.read("config.ini")
        self.frameCount = cf.getint("frames", "count")
        self.logfile = cf.get("run", "logfile")

    def metadataINFO(self):
        try:
            self.metadata = json.load(open("blocks/metadata.json", encoding="utf8"))
        except Exception:
            self.metadata = None
