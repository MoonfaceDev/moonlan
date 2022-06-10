from moonlan import consts
from moonlan.config import config
from moonlan.spoofing.arp_spoofing import ARPSpoofing
from moonlan.spoofing.exceptions import AlreadySpoofingError

DEFAULT_SPOOFED_DEVICE = {
    consts.ArpSpoofing.SPOOFED_DEVICE_MAC_KEY: consts.ArpSpoofing.SPOOFED_DEVICE_DEFAULT_MAC,
    consts.ArpSpoofing.SPOOFED_DEVICE_IP_KEY: consts.ArpSpoofing.SPOOFED_DEVICE_DEFAULT_IP,
    consts.ArpSpoofing.SPOOFED_DEVICE_FORWARD_KEY: consts.ArpSpoofing.SPOOFED_DEVICE_DEFAULT_FORWARD
}


class SpoofingManager:
    def __init__(self):
        self._arp_spoofing = None
        self._is_spoofing = False
        self._spoofed_device = DEFAULT_SPOOFED_DEVICE

    @property
    def is_spoofing(self):
        return self._is_spoofing

    @property
    def spoofed_device(self):
        return self._spoofed_device

    def start_spoof(self, ip: str, mac: str, forward: bool):
        if self._is_spoofing:
            raise AlreadySpoofingError()
        self._is_spoofing = True
        self._spoofed_device = {
            consts.ArpSpoofing.SPOOFED_DEVICE_MAC_KEY: mac,
            consts.ArpSpoofing.SPOOFED_DEVICE_IP_KEY: ip,
            consts.ArpSpoofing.SPOOFED_DEVICE_FORWARD_KEY: forward
        }
        self._arp_spoofing = ARPSpoofing(
            target_ip=ip,
            target_mac=mac,
            gateway_ip=config.spoofing.gateway_ip,
            gateway_mac=config.spoofing.gateway_mac,
            forward=forward
        )
        self._arp_spoofing.start()

    def stop_spoof(self):
        if self._is_spoofing:
            self._is_spoofing = False
            self._spoofed_device = DEFAULT_SPOOFED_DEVICE
            self._arp_spoofing.stop()
