import fs from "fs/promises";
import { Jimp } from "jimp";
import type { BmFont } from "@jimp/plugin-print/dist/esm/types";
import {
    SANS_32_BLACK,
    SANS_16_BLACK,
} from "@jimp/plugin-print/src/fonts";
import { loadConfig } from "../config";
import { BLOCK_SIZE, IMAGE_SIZE, SUBTITLE_SIZE } from "./constants";
import { drawTextCenteredInBox } from "./drawtil";
import {
    inputKeys,
    inputPosition,
    outputPosition,
    outputResultMap,
    outputTextMap,
    overwriteBlockSize,
} from "./position";

type JimpInstance = {
    bitmap: { width: number; height: number };
    setPixelColor: (color: number, x: number, y: number) => unknown;
    getPixelColor: (x: number, y: number) => number;
    print: (options: { font: BmFont; x: number; y: number; text: string | number }) => unknown;
    write: (path: `${string}.${string}`) => Promise<void>;
};

const INPUT_PATH = "blocks";
const OUTPUT_PATH = "assets/frames";
const USE_BACKGROUND = true;
const CROSS_LENGTH = 10;
const CROSS_WIDTH = 3;
const USE_BORDER = false;

function rgbToHex(r: number, g: number, b: number, a: number = 255): number {
    return (
        ((r & 0xff) << 24) |
        ((g & 0xff) << 16) |
        ((b & 0xff) << 8) |
        (a & 0xff)
    );
}

function drawHorizontalLine(
    image: JimpInstance,
    x1: number,
    y: number,
    x2: number,
    color: number,
    width: number,
): void {
    for (let w = 0; w < width; w++) {
        const currentY = y + w;
        for (let x = Math.min(x1, x2); x <= Math.max(x1, x2); x++) {
            if (x >= 0 && x < image.bitmap.width && currentY >= 0 && currentY < image.bitmap.height) {
                image.setPixelColor(color, x, currentY);
            }
        }
    }
}

function drawVerticalLine(
    image: JimpInstance,
    x: number,
    y1: number,
    y2: number,
    color: number,
    width: number,
): void {
    for (let w = 0; w < width; w++) {
        const currentX = x + w;
        for (let y = Math.min(y1, y2); y <= Math.max(y1, y2); y++) {
            if (currentX >= 0 && currentX < image.bitmap.width && y >= 0 && y < image.bitmap.height) {
                image.setPixelColor(color, currentX, y);
            }
        }
    }
}

function drawRectangle(
    image: JimpInstance,
    x: number,
    y: number,
    width: number,
    height: number,
    fillColor: number,
    outlineColor: number,
    outlineWidth: number,
): void {
    for (let py = 0; py < height; py++) {
        for (let px = 0; px < width; px++) {
            const drawX = x + px;
            const drawY = y + py;
            if (drawX >= 0 && drawX < image.bitmap.width && drawY >= 0 && drawY < image.bitmap.height) {
                const isOutline =
                    px < outlineWidth ||
                    px >= width - outlineWidth ||
                    py < outlineWidth ||
                    py >= height - outlineWidth;
                image.setPixelColor(isOutline ? outlineColor : fillColor, drawX, drawY);
            }
        }
    }
}

function drawCross(
    image: JimpInstance,
    centerX: number,
    centerY: number,
    length: number,
    color: number,
    width: number,
): void {
    drawHorizontalLine(
        image,
        centerX - length,
        centerY,
        centerX + length,
        color,
        width,
    );
    drawVerticalLine(
        image,
        centerX,
        centerY - length,
        centerY + length,
        color,
        width,
    );
}

async function loadFontFile(path: string): Promise<BmFont> {
    const { loadBitmapFontData, processBitmapFont } = await import(
        "@jimp/plugin-print/dist/esm/load-bitmap-font"
    );
    const data = await loadBitmapFontData(path);
    return processBitmapFont(path, data);
}

async function processImage(inputImage: JimpInstance, text: boolean): Promise<JimpInstance> {
    const outputImage = new Jimp({
        width: IMAGE_SIZE.width,
        height: IMAGE_SIZE.height,
        color: 0x00000000,
    });

    const colorMap: Record<string, number> = {};

    for (const key of inputKeys) {
        const realBlockSize = overwriteBlockSize[key] ?? BLOCK_SIZE;
        const [inputX, inputY] = inputPosition[key];
        const color = inputImage.getPixelColor(inputX, inputY);
        colorMap[key] = color;

        const [outputX, outputY] = outputPosition[key];

        drawRectangle(
            outputImage,
            outputX,
            outputY,
            realBlockSize,
            realBlockSize,
            color,
            rgbToHex(255, 0, 0),
            USE_BORDER ? 2 : 0,
        );

        drawCross(
            outputImage,
            outputX + realBlockSize / 2,
            outputY + realBlockSize / 2,
            CROSS_LENGTH,
            rgbToHex(255, 0, 0),
            CROSS_WIDTH,
        );
    }

    if (text) {
        const font = await loadFontFile(SANS_32_BLACK);
        const smallFont = await loadFontFile(SANS_16_BLACK);

        for (const key of inputKeys) {
            const realBlockSize = overwriteBlockSize[key] ?? BLOCK_SIZE;
            const [outputX, outputY] = outputPosition[key];

            drawTextCenteredInBox(
                outputImage,
                outputTextMap[key],
                [outputX, outputY, outputX + realBlockSize, outputY + realBlockSize],
                font,
            );

            drawTextCenteredInBox(
                outputImage,
                `T${outputResultMap[key]}:${key}`,
                [outputX, outputY + SUBTITLE_SIZE, outputX + realBlockSize, outputY + realBlockSize],
                smallFont,
            );
        }
    }

    return outputImage;
}

export async function generateFrames(): Promise<void> {
    const config = await loadConfig();
    const totalCount = config.frames.count;

    await fs.mkdir(OUTPUT_PATH, { recursive: true });

    let finishedCount = 0;

    if (USE_BACKGROUND) {
        const displayFrame = await Jimp.read(`${INPUT_PATH}/display_frame.png`);
        const processedFrame = await processImage(displayFrame, true);
        await processedFrame.write(`${OUTPUT_PATH}/display_frame.png`);
        finishedCount++;
    }

    for (let i = 0; i < totalCount; i++) {
        const inputImage = await Jimp.read(`${INPUT_PATH}/${i}.png`);
        const processedImage = await processImage(inputImage, false);
        await processedImage.write(`${OUTPUT_PATH}/${i}.png`);
        finishedCount++;
        process.stdout.write(`\r已完成${finishedCount}/${totalCount + (USE_BACKGROUND ? 1 : 0)}`);
    }
    console.log("");
}
