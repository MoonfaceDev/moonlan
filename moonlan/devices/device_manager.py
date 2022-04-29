import json
from pathlib import Path
from typing import Callable

from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from moonlan.devices.devices import DeviceEntry, Devices


class FileModifiedEventHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[FileModifiedEvent], None]):
        self._callback = callback

    def on_modified(self, event: FileModifiedEvent):
        self._callback(event)


class DevicesConfig:
    def __init__(self, config_path: Path):
        self._config_path = config_path
        self._devices = self._load_devices()

    @property
    def devices(self) -> Devices:
        return self._devices

    def listen_for_updates(self):
        def callback(_: FileModifiedEvent):
            self._devices = self._load_devices()

        observer = Observer()
        observer.schedule(FileModifiedEventHandler(callback), str(self._config_path))
        observer.start()

    def _load_devices(self) -> Devices:
        with self._config_path.open('r') as file:
            data = json.load(file)
            return Devices([DeviceEntry(**device) for device in data])


devices_config = DevicesConfig(Path('/etc/moonitor/api/devices.json').expanduser())
devices_config.listen_for_updates()
