import { BaseDroneServer, Oncable } from "../connection";
import { DRONE_ADDRESS, SEND_COMMAND_SERVER_ADDRESS } from "../constants";

export class PingServer extends BaseDroneServer implements Oncable {
    constructor() {
        super("udp4", DRONE_ADDRESS, SEND_COMMAND_SERVER_ADDRESS);
    }
    receive(): void { }
    async doOnce(): Promise<void> {
        try {
            await this.send("command");
            if (await this.waitMessage(5000) !== "ok") {
                throw new Error("响应无效");
            }
        } catch (err) {
            if (err instanceof Error) {
                console.error(`连接失败：${err.message}，请确保无人机已开启并连接至局域网。`);
            } else {
                console.error("发生未知错误。");
            };
        }
    }
}