from pydantic import BaseModel


class DevicesConfigUpdateRequest(BaseModel):
    data: str
