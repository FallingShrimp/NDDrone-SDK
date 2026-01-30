from psychopy import event, core
from loggers import loggerMain

flymode = True
neuroai = True


def prompt():
    if not flymode and not neuroai:
        loggerMain.info("所有任务已结束，按下任意键退出程序。")
        event.waitKeys()
        core.quit()
