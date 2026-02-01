import { imageSize, blockSize } from './constants';

export function top(distance: number): number {
    return distance;
}

export function bottom(distance: number): number {
    return imageSize[1] - blockSize - distance;
}

export function left(distance: number): number {
    return distance;
}

export function right(distance: number): number {
    return imageSize[0] - blockSize - distance;
}

export function center(offsetX: number, offsetY: number, blockSizeParam: number = blockSize): [number, number] {
    return [
        Math.floor(imageSize[0] / 2) - Math.floor(blockSizeParam / 2) + offsetX,
        Math.floor(imageSize[1] / 2) - Math.floor(blockSizeParam / 2) + offsetY,
    ];
}