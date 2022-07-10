from tkinter import Tk
from smarthome.device_base import DeviceBase, DeviceBaseView
from typing import Type


class App:
    root = Tk()
    devices = []
    views = []

    def __init__(self):
        self.root.geometry("1200x800")

    def run(self):
        for d in self.devices:
            d.run()
        try:
            self.root.mainloop()
        except Exception as e:
            print("Exception during GUI thread:", e)
        finally:
            self.cleanup()

    def add_device(self, device: DeviceBase, view: Type[DeviceBaseView]):
        self.devices.append(device)
        f = view(self.root)
        f.pack()
        device.set_view(f)
        self.views.append(f)

    def cleanup(self):
        for d in self.devices:
            try:
                d.stop()
            except Exception as e:
                print(e)
