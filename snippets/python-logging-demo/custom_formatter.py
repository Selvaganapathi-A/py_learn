import logging
from typing import Any, Literal, Mapping


class BashFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self._color_fmts = {
            0: "\x1b[38;5;255m",
            10: "\x1b[38;5;2m",
            20: "\x1b[38;5;82m",
            30: "\x1b[38;5;226m",
            40: "\x1b[1;38;5;208m",
            50: "\x1b[1;21;38;5;245m",  #  \x1B[48;5;196m
        }

    def format(self, record: logging.LogRecord) -> str:
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return self._color_fmts.get(record.levelno, "") + s + "\x1b[0m"
