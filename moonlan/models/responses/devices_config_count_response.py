from pydantic import BaseModel


class DevicesConfigCountResponse(BaseModel):
    count: int
