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
export const disableKeys = ["land", "flip"];
export const outputPosition: Record<string, [number, number]> = {
    "up": [left(Math.floor(250 / 2)), center(0, 0, 250)[1]],
    "down": [right(Math.floor(250 / 2)), center(0, 0, 250)[1]],
    "left": [right(0), top(0)],
    "right": [right(0), bottom(0)],
    "forward": [left(0), top(0)],
    "back": [left(0), bottom(0)],
    "takeoff": center(0, 0, 500),
    "land": [left(0), bottom(0)],
    "flip": [right(0), bottom(0)]
};
export const outputTextMap: Record<string, string> = {
    "up": "短上",
    "down": "短下",
    "left": "短左",
    "right": "短右",
    "forward": "短前",
    "back": "短后",
    "takeoff": "步进",
    "land": "",
    "flip": "",
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
    "takeoff": 500,
    "up": 250,
    "down": 250,
};
export const inputKeys = Object.keys(inputPosition).filter(key => !disableKeys.includes(key));