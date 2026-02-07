import { program } from "commander";
import { detachable, input, safeExecute } from "./util";
import process from "process";
import childProcess from "child_process";
import packageData from "../../package.json";
import { CommandServer } from "./servers/command";
import { DroneStateServer } from "./servers/droneState";
import { PingServer } from "./servers/ping";
import { generateFrames, generateMetadatas } from "./generator/generate";

async function main() {
    program
        .name(packageData.name)
        .version(packageData.version)
        .description(packageData.description);
    const startCommand = program.command("start")
        .action(() => safeExecute("python ./src/index.py"));
    startCommand.command("neuroapi")
        .action(() => safeExecute("python ./src/entry/neuroApi.py"));
    startCommand.command("flymode")
        .action(() => safeExecute("python ./src/entry/flymode.py"));
    program.command("generate")
        .action(async () => {
            await generateFrames();
            await generateMetadatas();
        });
    program.command("command")
        .action(async () => {
            console.log("--- NDDrone-SDK 无人机交互终端 ---");
            process.stdout.write("正在连接无人机...");
            const commandServer = new CommandServer();
            const pingServer = new PingServer();
            await pingServer.doOnce();
            console.log("连接成功。");
            while (true) {
                await detachable(async () => {
                    commandServer.send(await input("> "));
                });
            }
        });
    program.command("state")
        .option("-w, --watch", "是否持续视奸无人机状态", false)
        .action(async (options: { watch: boolean }) => {
            const droneState = new DroneStateServer();
            process.stdout.write("正在连接无人机...");
            await detachable(async () => {
                await droneState.initialize();
            });
            console.log("连接成功。");
            do {
                console.log(droneState.toString());
            } while (options.watch);
            droneState.stop();
        });

    program.parse(process.argv);
}
main();
