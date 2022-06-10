from pydantic import BaseModel

from moonlan import consts


class DeviceEntry(BaseModel):
    name: str
    mac: str
    type: str


def get_default_device(mac: str) -> DeviceEntry:
    return DeviceEntry(name=consts.DeviceManager.DEFAULT_NAME, mac=mac, type=consts.DeviceManager.DEFAULT_TYPE)


class Devices(list[DeviceEntry]):
    def __getitem__(self, name: str) -> DeviceEntry:
        for entry in self:
            if entry.name.lower() == name.lower():
                return entry
        raise KeyError(name)

    def from_mac(self, mac: str) -> DeviceEntry:
        for entry in self:
            if entry.mac.lower() == mac.lower():
                return entry
        return get_default_device(mac)

    def __len__(self) -> int:
        return super().__len__()
