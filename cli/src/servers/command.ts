import { writeFile } from "fs/promises";
import { BaseDroneServer } from "../connection";
import { DRONE_ADDRESS, SEND_COMMAND_SERVER_ADDRESS2 } from "../constants";

export class CommandServer extends BaseDroneServer {
    constructor() {
        super("udp4", DRONE_ADDRESS, SEND_COMMAND_SERVER_ADDRESS2);
    }
    receive(message: string): void {
        writeFile("1.txt", message);
    }
}