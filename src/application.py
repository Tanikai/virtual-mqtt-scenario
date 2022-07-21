import tkinter as tk
from tkinter import messagebox
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
    device_count = [0, 0, 0, 0, 0]

    def __init__(self):
        """Constructor for the App class."""
        self.root.geometry("1200x800")
        self.bt_start = tk.Button(self.root,
                                  text="Start Scenario",
                                  command=self.start_scenario)
        self.bt_start.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
        self.fr_devices = tk.Frame(self.root, background="white",
                                   borderwidth=2, relief="ridge")
        self.fr_devices.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

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
        try:
            self.explorer.run()
            for d in self.devices:
                d.run()
        except ConnectionError as e:
            messagebox.showerror("Connection to MQTT broker failed",
                                 "Connection to MQTT broker failed; not "
                                 "started or wrong host/port?")
            print("Could not connect to MQTT broker, message:", e)
            self.cleanup()

    def add_device(self, device: DeviceBase, view: Type[DeviceBaseView],
                   d_col=0):
        """
        Adds a new device to the simulation.
        :param device: An *instance* of a device. Configuration can be done
        before or after adding.
        :param view: A *class reference* to the view class that is used for the
        device.
        :param d_col: Column for device.
        :return: A reference to the added device for convenience.
        """
        self.devices.append(device)
        f = view(self.fr_devices)  # create instance of view
        f.grid(column=d_col, row=self.device_count[d_col], pady=5, padx=5,
               sticky="nsew")
        self.device_count[d_col] += 1
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
