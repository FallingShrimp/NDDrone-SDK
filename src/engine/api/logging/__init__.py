import datetime

import rich
import json
from pydantic import BaseModel, FieldSerializationInfo, field_serializer
from typing import Union
from engine.api.logging.constants import MESSAGETYPE_COLOR_MAP, MessageType
from engine.api.timer import format


class LogRecord(BaseModel):
    type: MessageType
    message: str
    time: datetime.datetime
    moduleName: str

    @field_serializer("time")
    def serialize_time(self, dt: datetime.datetime, _info: FieldSerializationInfo):
        return dt.isoformat()

    def __init__(
        self,
        type: MessageType = MessageType.INFO,
        message: str = "",
        moduleName: str = "main",
    ):
        super().__init__(
            type=type,
            message=message,
            time=datetime.datetime.now(),
            moduleName=moduleName,
        )

    def print(self):
        color = MESSAGETYPE_COLOR_MAP[self.type]
        rich.print(
            f"[white][cyan]{format(self.time)}[magenta]<{self.moduleName}>[/magenta][/cyan] [{color}]\\[{self.type.name}][/{color}] {self.message}[/white]"
        )


class Logger:
    records: list[LogRecord]
    moduleName: str
    parent: Union["Logger", None]

    def __init__(self, moduleName: str, parent: Union["Logger", None] = None) -> None:
        self.records = []
        self.moduleName = moduleName
        self.parent = parent

    def toRaw(self) -> list[dict]:
        return [record.model_dump() for record in self.records]

    def modulePath(self) -> str:
        return (
            self.moduleName
            if self.parent is None
            else f"{self.parent.modulePath()}.{self.moduleName}"
        )

    def export(self, to: str):
        self.info(f"正在导出日志到{to}...")
        with open(to, "w", encoding="utf8") as f:
            json.dump(self.toRaw(), f, ensure_ascii=False, indent=4)

    def log(self, type: MessageType, *messages: str):
        record = LogRecord(type, " ".join(messages), self.modulePath())
        self.records.append(record)
        if self.parent:
            self.parent.records.append(record)
        record.print()

    def info(self, message: str):
        self.log(MessageType.INFO, message)

    def warning(self, message: str):
        self.log(MessageType.WARNING, message)

    def error(self, *messages: str | Exception):
        self.log(MessageType.ERROR, *[str(x) for x in messages])


loggerMain = Logger("main")
