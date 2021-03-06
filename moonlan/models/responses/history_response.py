from datetime import datetime

from pydantic import BaseModel


class HistoryRecord(BaseModel):
    time: datetime
    average: float | None


class HistoryResponse(BaseModel):
    __root__: list[HistoryRecord]
