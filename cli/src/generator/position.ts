import { top, bottom, left, right, center } from "./anchor";

export const inputPosition: Record<string, [number, number]> = {
    "up": [630, 110],
    "down": [630, 750],
    "left": [950, 430],
    "right": [1590, 430],
    "forward": [1260, 110],
    "back": [1260, 750],
    "takeoff": [30, 110],
    "land": [30, 750],
    "flip": [330, 430],
};
export const disableKeys: string[] = [];
export const outputPosition: Record<string, [number, number]> = {
    "up": [left(0), top(0)],
    "down": [right(0), top(0)],
    "left": [left(0), bottom(0)],
    "right": [right(0), bottom(0)],
    "forward": [left(0), center(0, 0)[1]],
    "back": [right(0), center(0, 0)[1]],
    "takeoff": [center(0, 0)[0], top(0)],
    "land": [center(0, 0)[0], bottom(0)],
    "flip": center(0, 0)
};
export const outputTextMap: Record<string, string> = {
    "up": "Block1",
    "down": "Block2",
    "left": "Block3",
    "right": "Block4",
    "forward": "Block5",
    "back": "Block6",
    "takeoff": "Block7",
    "land": "Block8",
    "flip": "Block9",
};
export const outputResultMap: Record<string, number> = {
    "up": 1,
    "down": 3,
    "left": 7,
    "right": 5,
    "forward": 4,
    "back": 6,
    "takeoff": 0,
    "land": 2,
    "flip": 8,
};
export const overwriteBlockSize: Record<string, number> = {
};
export const inputKeys = Object.keys(inputPosition).filter(key => !disableKeys.includes(key));
