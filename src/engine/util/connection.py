from socket import AddressFamily, SocketKind, socket

from loggers import loggerOthers


def connectSocket(
    address: tuple[str, int],
    retryTimes: int,
    af: AddressFamily = AddressFamily.AF_INET,
    type: SocketKind = SocketKind.SOCK_STREAM,
) -> socket:
    resultSocket = socket(af, type)
    connected = False
    reconnectedTimes = 0
    while not connected:
        try:
            resultSocket.connect(address)
            connected = True
        except Exception:
            reconnectedTimes += 1
            if reconnectedTimes > retryTimes:
                loggerOthers.warning(f"Cannot connect to {address}.")
                break
    return resultSocket


def isConnected(socket: socket) -> bool:
    try:
        socket.getpeername()
        return True
    except Exception:
        return False
