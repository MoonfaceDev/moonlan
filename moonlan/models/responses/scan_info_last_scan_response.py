from datetime import datetime

from pydantic import BaseModel


class ScanInfoLastScanResponse(BaseModel):
    last_scan: datetime
