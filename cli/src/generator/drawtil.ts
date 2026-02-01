import type { JimpClass } from "@jimp/types";
import type { BmFont } from "@jimp/plugin-print/dist/esm/types";

export function drawTextCenteredInBox(
    image: JimpClass & { print: (options: { font: BmFont; x: number; y: number; text: string | number }) => unknown },
    text: string,
    rect: [number, number, number, number],
    font: BmFont,
): void {
    const [x1, y1, x2, y2] = rect;
    const width = x2 - x1;
    const height = y2 - y1;

    const textWidth = (font as unknown as { getWidth: (text: string) => number }).getWidth(text);
    const textHeight = (font as unknown as { getHeight: (text: string) => number }).getHeight(text);

    const x = x1 + (width - textWidth) / 2;
    const y = y1 + (height - textHeight) / 2;

    image.print({ font, x: Math.floor(x), y: Math.floor(y), text });
}

export function measureText(font: BmFont, text: string): { width: number; height: number } {
    const fontWithMethods = font as unknown as { getWidth: (text: string) => number; getHeight: (text: string) => number };
    return {
        width: fontWithMethods.getWidth(text),
        height: fontWithMethods.getHeight(text),
    };
}
