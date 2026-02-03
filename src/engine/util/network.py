from socket import AddressFamily, SocketKind, socket

from engine.util.original import retry
from instances.loggers import loggerNetwork


def createServer(
    address: tuple[str, int],
    af: AddressFamily = AddressFamily.AF_INET,
    type: SocketKind = SocketKind.SOCK_STREAM,
) -> socket:
    result = socket(af, type)
    result.bind(address)
    result.listen(1)
    return result


def waitClient(
    serverSocket: socket, maxRetryTimes: int
) -> tuple[socket, tuple[str, int]]:
    loggerNetwork.info(f"等待客户端连接到{serverSocket.getsockname()}...")

    @retry(maxRetryTimes)
    def tryAccept():
        try:
            return serverSocket.accept()
        except Exception:
            return False

    result, state = tryAccept()
    if state:
        return result
    else:
        loggerNetwork.warning(f"接受客户端连接失败{serverSocket.getsockname()}。")
        return emptyTcp(), emptyAddress()


def emptyTcp():
    return socket(AddressFamily.AF_INET, SocketKind.SOCK_STREAM)


def emptyAddress():
    return ("", 0)


def createClient(address: tuple[str, int], maxRetryTimes: int) -> socket:
    loggerNetwork.info(f"正在连接到{address}...")

    @retry(maxRetryTimes)
    def tryConnect():
        try:
            resultSocket = emptyTcp()
            resultSocket.connect(address)
            return resultSocket
        except Exception:
            return False

    result, state = tryConnect()
    if state:
        return result
    else:
        loggerNetwork.warning(f"连接到{address}失败。")
        return emptyTcp()


def checkConnection(clientSocket: socket) -> bool:
    try:
        clientSocket.getpeername()
        return True
    except Exception:
        return False
