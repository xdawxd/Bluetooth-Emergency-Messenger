import bluetooth

from typing import List, Union

from PyOBEX.client import Client


class OBEXConnection:
    def __init__(self, client: Client):
        self.connection = client

    def __enter__(self):
        print("Connected!")
        return self.connection.connect()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Disconnected!")
        self.connection.disconnect()


class BEM:
    OBEX_ANDROID_PORT: int = 12

    def __init__(self, devices: List[str], file_content: str):
        self._devices = self._get_devices(devices)
        self._file_content = file_content
        self._notified_devices: List[str] = []

    @property
    def _nearby_devices(self) -> list:  # TODO - check if the args are necessary
        print("Searching for devices.")
        return bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    @staticmethod
    def _get_devices(devices: List[str]) -> Union[List[str], str]:
        return devices[0] if len(devices) == 1 else devices

    def _selected_device(self, name: str) -> bool:
        print("Validating devices.")
        if not isinstance(devices := self._devices, list):
            return name == devices
        return name in devices

    @staticmethod
    def get_device_services(address: str) -> None:
        for service in bluetooth.find_service(address):
            print(service)

    def get_nearby_devices(self) -> None:
        print(f"Found: {len(self._nearby_devices)}")
        for address, name in self._nearby_devices:
            print(f"{address} - {name}")

    def get_device_addresses(self) -> List[str]:
        return [address for address, name in self._nearby_devices if self._selected_device(name)]

    def _send_message_file(self, address: str) -> None:
        print("Sending file.")
        client = Client(address, self.OBEX_ANDROID_PORT)
        with OBEXConnection(client):
            client.put("test.txt", bytes(self._file_content, "utf-8"))  # Might fail
            print("Text file sent!")

    def process(self) -> None:
        while True:
            addresses = self.get_device_addresses()
            for address in addresses:
                if address not in self._notified_devices and isinstance(self._devices, list):
                    print("Excluding devices.")
                    self._notified_devices.append(address)
                    continue
                print(address)
                self._send_message_file(address)
            else:
                break
