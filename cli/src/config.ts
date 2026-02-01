import { parse } from "ini";
import fs from "fs/promises";

export async function loadConfig(): Promise<ConfigData> {
    const configText = await fs.readFile("config.ini", "utf-8");
    const result = parse(configText) as ConfigData;
    result.frames.count = Number(result.frames.count);
    if (isNaN(result.frames.count)) {
        console.error("frames.count必须为数字");
        process.exit(1);
    }
    result.run.threads = Number(result.run.threads);
    if (isNaN(result.run.threads)) {
        console.error("run.threads必须为数字");
        process.exit(1);
    }
    return result;
}
export interface ConfigData {
    frames: {
        count: number;
    };
    run: {
        logfile: string;
        threads: number;
    };
}