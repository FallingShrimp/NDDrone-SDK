import { IMAGE_SIZE, BLOCK_SIZE } from "./constants";

export function top(distance: number): number {
    return distance;
}

export function bottom(distance: number): number {
    return IMAGE_SIZE.height - BLOCK_SIZE - distance;
}

export function left(distance: number): number {
    return distance;
}

export function right(distance: number): number {
    return IMAGE_SIZE.width - BLOCK_SIZE - distance;
}

export function center(offsetX: number, offsetY: number, blockSize: number = BLOCK_SIZE): [number, number] {
    return [
        IMAGE_SIZE.width / 2 - blockSize / 2 + offsetX,
        IMAGE_SIZE.height / 2 - blockSize / 2 + offsetY,
    ];
}
