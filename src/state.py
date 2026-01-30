from psychopy import core
from loggers import loggerMain

flymode = True
neuroapi = True


def prompt():
    loggerMain.info(
        f"飞控：{formatAsSwitch(flymode)}，NeuroAPI：{formatAsSwitch(neuroapi)}"
    )
    if not flymode and not neuroapi:
        loggerMain.info("所有组件已停止运行，按下Enter退出程序。")
        input("")
        core.quit()


def formatAsSwitch(state: bool) -> str:
    return "[green]正在运行[/green]" if state else "[red]已停止[/red]"
