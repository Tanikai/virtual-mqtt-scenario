import tkinter as tk
from smarthome.device_base import DeviceBase, DeviceBaseView
from typing import Type
from explorer import Explorer, ExplorerView


class App:
    """
    This is the main "controller" of the application. It owns all simulated
    devices and the root tkinter view.
    """
    root = tk.Tk()
    fr_devices = None
    devices = []
    views = []

    def __init__(self):
        """Constructor for the App class."""
        self.root.geometry("1200x800")
        self.bt_start = tk.Button(self.root,
                                  text="Start Scenario",
                                  command=self.start_scenario)
        self.bt_start.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
        self.fr_devices = tk.Frame(self.root, background="white")
        self.fr_devices.pack(side=tk.LEFT, fill=tk.BOTH)

        self.fr_explorer = ExplorerView(self.root)
        self.fr_explorer.pack(side=tk.RIGHT, anchor=tk.NE, padx=5, pady=5,
                              fill=tk.BOTH, expand=True)
        self.explorer = Explorer()
        self.explorer.set_view(self.fr_explorer)

    def run(self):
        """Runs the tkinter GUI of the application."""
        try:
            self.root.mainloop()
        except Exception as e:
            print("Exception during GUI thread:", e)
        finally:
            self.cleanup()

    def start_scenario(self):
        """This method runs the simulation by running all devices."""
        self.bt_start.config(state=tk.DISABLED)
        self.explorer.run()
        for d in self.devices:
            d.run()

    def add_device(self, device: DeviceBase, view: Type[DeviceBaseView]):
        """
        Adds a new device to the simulation.
        :param device: An *instance* of a device. Configuration can be done
        before or after adding.
        :param view: A *class reference* to the view class that is used for the
        device.
        :return: A reference to the added device for convenience.
        """
        self.devices.append(device)
        f = view(self.fr_devices)
        f.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5, fill=tk.X)
        device.set_view(f)
        self.views.append(f)
        return device

    def cleanup(self):
        """Stops all devices."""
        for d in self.devices:
            try:
                d.stop()
            except Exception as e:
                print(e)
