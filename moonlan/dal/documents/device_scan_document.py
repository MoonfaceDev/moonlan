from datetime import datetime

from pydantic import BaseModel


class DeviceScanDocument(BaseModel):
    scan_time: datetime
    online: bool
