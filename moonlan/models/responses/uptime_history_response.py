from datetime import datetime, timedelta

from pydantic import BaseModel


class UptimeRecord(BaseModel):
    time: datetime
    uptime: timedelta


class UptimeHistoryResponse(BaseModel):
    __root__: list[UptimeRecord]
