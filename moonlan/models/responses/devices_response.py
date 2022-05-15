from pydantic import BaseModel

from moonlan.models.responses.device_response import DeviceResponse


class DevicesResponse(BaseModel):
    __root__: list[DeviceResponse]
