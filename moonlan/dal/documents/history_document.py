from datetime import datetime

from pydantic import BaseModel


class HistoryDocument(BaseModel):
    id: datetime
    avg: float

    class Config:
        fields = {'id': '_id'}
