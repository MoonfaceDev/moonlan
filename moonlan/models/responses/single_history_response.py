from datetime import datetime, timedelta

from pydantic import BaseModel


class SingleHistoryRecord(BaseModel):
    time: datetime
    online_time: timedelta


class SingleHistoryResponse(BaseModel):
    __root__: list[SingleHistoryRecord]
