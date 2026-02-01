def topLeftToCenter(topLeft: tuple[int, int], size: tuple[int, int]) -> list[int]:
    width, height = size
    xTL, yTL = topLeft
    xCenter = xTL - width // 2
    yCenter = -(yTL - height // 2)
    return [xCenter, yCenter]
