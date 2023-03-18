from bluetooth_connection import BEM

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

kivy.require("2.1.0")  # TODO - check if its necessary to do that


class MyRoot(BoxLayout):

    def __init__(self):
        super().__init__()

    def connect_via_bluetooth(self):
        devices = [device.strip() for device in self.devices.text.split(",")]
        file_content = self.file_content.text
        print(devices, file_content)
        bem = BEM(devices, file_content)
        bem.process()


class BEMApp(App):
    def build(self):
        return MyRoot()


if __name__ == "__main__":
    bem_app = BEMApp()
    bem_app.run()
