import * as fs from "fs";
import * as path from "path";
import * as PI from "pureimage";
import { Pool, spawn, Worker } from "threads";
import { blockSize, imageSize, subtitleSize } from "./constants";
import { drawTextCenteredInBox } from "./drawtil";
import { inputKeys, inputPosition, outputPosition, outputResultMap, outputTextMap, overwriteBlockSize } from "./position";
import { loadConfig } from "../config";
import { progressBar } from "../util";

export async function process(inputImagePath: string, text: boolean): Promise<PI.Bitmap> {
    const inputImage = await PI.decodePNGFromStream(fs.createReadStream(inputImagePath));
    const outputImage = PI.make(imageSize[0], imageSize[1]);
    const ctx = outputImage.getContext("2d");
    const colorMap: Record<string, number> = {};
    const crossLength = 10;
    const crossWidth = 3;
    const useBorder = false;
    for (const key of inputKeys) {
        const realBlockSize = overwriteBlockSize[key] || blockSize;
        const [x, y] = inputPosition[key];
        const pixel = inputImage.getPixelRGBA(x, y);
        colorMap[key] = pixel;
        const [outputX, outputY] = outputPosition[key];
        ctx.fillStyle = `#${pixel.toString(16).padStart(8, "0")}`;
        ctx.fillRect(outputX, outputY, realBlockSize, realBlockSize);
        if (useBorder) {
            ctx.strokeStyle = "rgba(255, 0, 0, 255)";
            ctx.lineWidth = 1;
            ctx.strokeRect(outputX, outputY, realBlockSize, realBlockSize);
        }
        ctx.strokeStyle = "rgba(255, 0, 0, 255)";
        ctx.lineWidth = crossWidth;
        ctx.beginPath();
        ctx.moveTo(outputX - crossLength + realBlockSize / 2, outputY + realBlockSize / 2);
        ctx.lineTo(outputX + crossLength + realBlockSize / 2, outputY + realBlockSize / 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(outputX + realBlockSize / 2, outputY - crossLength + realBlockSize / 2);
        ctx.lineTo(outputX + realBlockSize / 2, outputY + crossLength + realBlockSize / 2);
        ctx.stroke();
    }
    if (text) {
        for (const key of inputKeys) {
            const realBlockSize = overwriteBlockSize[key] || blockSize;
            const [outputX, outputY] = outputPosition[key];
            drawTextCenteredInBox(
                outputImage,
                outputTextMap[key],
                [outputX, outputY, outputX + realBlockSize, outputY + realBlockSize],
                50,
                [0, 0, 0, 255]
            );
            drawTextCenteredInBox(
                outputImage,
                `T${outputResultMap[key]}:${key}`,
                [outputX, outputY + subtitleSize, outputX + realBlockSize, outputY + realBlockSize],
                35,
                [100, 100, 100, 255]
            );
        }
    }
    return outputImage;
}
export async function frame(index: number, inputPath: string, outputPath: string): Promise<void> {
    const inputImagePath = path.join(inputPath, `${index}.png`);
    const outputImagePath = path.join(outputPath, `${index}.png`);
    const outputImage = await process(inputImagePath, false);
    await PI.encodePNGToStream(outputImage, fs.createWriteStream(outputImagePath));
}
export async function generate(): Promise<void> {
    const config = await loadConfig();
    const inputPath = "blocks";
    const outputPath = "assets/frames";
    const totalCount = config.frames.count;
    const threadCount = Math.min(8, totalCount);
    if (!fs.existsSync(outputPath)) {
        fs.mkdirSync(outputPath, { recursive: true });
    }
    const inputImagePath = path.join(inputPath, "display_frame.png");
    const outputImagePath = path.join(outputPath, "display_frame.png");
    const outputImage = await process(inputImagePath, true);
    await PI.encodePNGToStream(outputImage, fs.createWriteStream(outputImagePath));
    const pool = Pool(() => spawn(new Worker("./worker")), threadCount);
    try {
        const tasks = [];
        for (let i = 0; i < totalCount; i++) {
            tasks.push(pool.queue(async (worker) => {
                const result = await worker.frameWorker({
                    index: i,
                    inputPath,
                    outputPath
                });
                return result;
            }));
        }
        let finishedCount = 1;
        const promises = tasks.map(async (task) => {
            await task;
            finishedCount++;
            global.process.stdout.write(`已完成${finishedCount}/${totalCount + 1} ${progressBar(finishedCount / (totalCount + 1) * 100, 10)}\r`);
        });
        await Promise.all(promises);
        console.log("\n所有帧已处理完成");
    } finally {
        await pool.terminate();
    }
}
if (require.main === module) {
    generate().catch(err => {
        console.error("生成过程中出错:", err);
    });
}