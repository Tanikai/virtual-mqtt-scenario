import tkinter as tk
from smarthome.device_base import DeviceBase, DeviceBaseView
from typing import Type


class App:
    root = tk.Tk()
    fr_devices = None
    devices = []
    views = []

    def __init__(self):
        self.root.geometry("1200x800")
        self.bt_start = tk.Button(self.root,
                                  text="Start Scenario",
                                  command=self.start_scenario)
        self.bt_start.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
        self.fr_devices = tk.Frame(self.root)
        self.fr_devices.pack(fill=tk.BOTH, expand=True)

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print("Exception during GUI thread:", e)
        finally:
            self.cleanup()

    def start_scenario(self):
        self.bt_start.config(state=tk.DISABLED)
        for d in self.devices:
            d.run()

    def add_device(self, device: DeviceBase, view: Type[DeviceBaseView]):
        self.devices.append(device)
        f = view(self.fr_devices)
        f.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5)
        device.set_view(f)
        self.views.append(f)

    def cleanup(self):
        for d in self.devices:
            try:
                d.stop()
            except Exception as e:
                print(e)
