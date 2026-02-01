from engine.api.logging import Logger

totalLogger = Logger("Logger")
loggerMain = Logger("FlymodeMain", totalLogger)
loggerBehaviour = Logger("CommandBehaviour", totalLogger)
loggerDrone = Logger("RoboMaster", totalLogger)
loggerNeuroApi = Logger("NeuroAPI", totalLogger)
loggerTaskQueue = Logger("TaskQueue", totalLogger)
loggerDevice = Logger("Device", totalLogger)
loggerNetwork = Logger("Network", totalLogger)
loggerRenderer = Logger("Renderer", totalLogger)
