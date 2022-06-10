from pydantic import BaseModel


class ScanInfoIntervalResponse(BaseModel):
    interval: float
