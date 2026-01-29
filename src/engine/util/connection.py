from socket import AddressFamily, SocketKind, socket

from engine.util.original import retry
from loggers import loggerOthers


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
    loggerOthers.info(
        f"Waiting for client connection on {serverSocket.getsockname()}..."
    )

    @retry(maxRetryTimes)
    def tryAccept():
        try:
            clientSocket, clientAddr = serverSocket.accept()
            return clientSocket, clientAddr
        except Exception:
            return False

    result, state = tryAccept()
    if not state:
        loggerOthers.warning(
            f"Failed to accept client connection on {serverSocket.getsockname()}."
        )
    return result


def createClient(
    address: tuple[str, int],
    maxRetryTimes: int,
    af: AddressFamily = AddressFamily.AF_INET,
    type: SocketKind = SocketKind.SOCK_STREAM,
) -> socket:
    loggerOthers.info(f"Connecting to {address}...")

    @retry(maxRetryTimes)
    def tryConnect():
        try:
            resultSocket = socket(af, type)
            resultSocket.connect(address)
            return resultSocket
        except Exception:
            return False

    result, state = tryConnect()
    if not state:
        loggerOthers.warning(f"Failed to connect to {address}.")
    return result


def checkConnection(clientSocket: socket) -> bool:
    try:
        clientSocket.getpeername()
        return True
    except Exception:
        return False
