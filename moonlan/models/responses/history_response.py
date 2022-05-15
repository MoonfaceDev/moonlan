from pydantic import BaseModel


class HistoryResponse(BaseModel):
    time: str
    average: float
