from pydantic import BaseModel


class HistoryRecord(BaseModel):
    time: str
    average: float


class HistoryResponse(BaseModel):
    __root__: list[HistoryRecord]
