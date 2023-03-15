import bluetooth

from typing import List

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

    def __init__(self, devices: List[str]):
        self._devices = devices
        self._notified_devices: List[str] = []

    @property
    def _nearby_devices(self) -> list:
        return bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    @staticmethod
    def get_device_services(address: str) -> None:
        for service in bluetooth.find_service(address):
            print(service)

    def get_nearby_devices(self) -> None:
        print(f"Found: {len(self._nearby_devices)}")
        for address, name in self._nearby_devices:
            print(f"{address} - {name}")

    def get_device_addresses(self) -> List[str]:
        return [address for address, name in self._nearby_devices if name in self._devices]

    def _send_message_file(self, address: str) -> None:
        client = Client(address, self.OBEX_ANDROID_PORT)
        with OBEXConnection(client):
            client.put("test.txt", b"Hello world\n")
            print("Text file sent!")

    def process(self):
        while True:
            addresses = self.get_device_addresses()
            for address in addresses:
                if address in self._notified_devices:
                    continue
                print(address)
                self._send_message_file(address)
            else:
                break


if __name__ == "__main__":
    bluetooth_devices = ["Kacper", "Kacper2", "Y", "OPPO Reno6 5G"]
    bem = BEM(bluetooth_devices)
    bem.process()
