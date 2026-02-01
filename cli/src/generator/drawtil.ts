import * as PI from "pureimage";
import opentype from "opentype.js";

const font = opentype.loadSync("C:/Windows/Fonts/Deng.ttf");

export function drawTextCenteredInBox(
    img: PI.Bitmap,
    text: string,
    rect: [number, number, number, number],
    fontSize: number,
    fill: [number, number, number, number]
): void {
    const ctx = img.getContext("2d");
    const path = font.getPath(text, 0, 0, fontSize);
    const bbox = path.getBoundingBox();
    const width = bbox.x2 - bbox.x1;
    const height = bbox.y2 - bbox.y1;
    const x = rect[0] + (rect[2] - rect[0] - width) / 2 - bbox.x1;
    const y = rect[1] + (rect[3] - rect[1] - height) / 2 - bbox.y1;
    ctx.fillStyle = `rgba(${fill[0]}, ${fill[1]}, ${fill[2]}, ${fill[3] / 255})`;
    const drawPath = font.getPath(text, x, y, fontSize);
    drawPath.draw(ctx as unknown as CanvasRenderingContext2D);
}