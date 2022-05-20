from datetime import datetime

from pydantic import BaseModel


class SingleDeviceScanDocument(BaseModel):
    scan_time: datetime
    online: bool
