from datetime import datetime, timedelta

from pydantic import BaseModel


class UptimeRecord(BaseModel):
    time: datetime
    uptime: timedelta | None


class UptimeHistoryResponse(BaseModel):
    __root__: list[UptimeRecord]
