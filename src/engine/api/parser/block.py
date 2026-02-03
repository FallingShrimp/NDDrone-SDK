from engine.util.original import readKeyByValue
from instances.config import config


def blockPosition(resultIndex: int) -> tuple[int, int]:
    if config.metadata:
        blockX, blockY = config.metadata["outputPosition"][
            readKeyByValue(
                config.metadata["outputResultMap"],
                resultIndex,
            )
        ]
        return blockX, blockY
    else:
        return 0, 0


def blockSize(resultIndex: int) -> tuple[int, int]:
    if config.metadata:
        length = config.metadata["overwriteBlockSize"].get(
            readKeyByValue(
                config.metadata["outputResultMap"],
                resultIndex,
            ),
            config.metadata["blockSize"],
        )
        return length, length
    else:
        return 0, 0
