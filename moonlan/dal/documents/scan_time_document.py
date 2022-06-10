from datetime import datetime

from pydantic import BaseModel


class ScanTimeDocument(BaseModel):
    scan_time: datetime
