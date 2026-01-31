from psychopy import core
from config import config
from loggers import loggerMain, totalLogger

flymode = True
neuroapi = True


def prompt():
    loggerMain.info(
        f"飞控：{formatAsSwitch(flymode)}，NeuroAPI：{formatAsSwitch(neuroapi)}"
    )
    if not flymode and not neuroapi:
        totalLogger.export(config.logfile)
        core.quit()


def formatAsSwitch(state: bool) -> str:
    return "[green]正在运行[/green]" if state else "[red]已停止[/red]"
