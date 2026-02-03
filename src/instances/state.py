from psychopy import core

from instances.config import config
from instances.loggers import totalLogger

flymode = True
neuroapi = True


def prompt():
    totalLogger.info(
        f"飞控：{formatAsSwitch(flymode)}，NeuroAPI：{formatAsSwitch(neuroapi)}"
    )
    if not flymode and not neuroapi:
        totalLogger.export(config.logfile)
        core.quit()


def formatAsSwitch(state: bool) -> str:
    return "[green]正在运行[/green]" if state else "[red]已停止[/red]"
