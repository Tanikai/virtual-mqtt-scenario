import tkinter as tk
from tkinter import messagebox
from smarthome.device_base import DeviceBase, DeviceBaseView
from typing import Type
from explorer import Explorer, ExplorerView
from message_publisher import MessagePublisher, MessagePublisherView


class App:
    """
    This is the main "controller" of the application. It owns all simulated
    devices and the root tkinter view.
    """
    root = tk.Tk()
    fr_devices = None
    devices = []
    views = []
    device_cols = []

    def __init__(self, server_info: dict):
        """Constructor for the App class."""
        self.root.title("Virtual MQTT Simulation")
        self.root.geometry("1600x900")
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
        self.explorer = Explorer(server_info)
        self.explorer.set_view(self.fr_explorer)

        for i in range(0, 4):  # create 5 columns
            column = tk.Frame(self.fr_devices, background="white")
            column.grid(row=0, column=i, sticky="nsew")
            self.device_cols.append(column)

        self.fr_msg_publisher = MessagePublisherView(self.device_cols[0])
        self.fr_msg_publisher.pack(side=tk.TOP, fill=tk.X)
        self.msg_publisher = MessagePublisher(server_info)
        self.msg_publisher.set_view(self.fr_msg_publisher)

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
            self.msg_publisher.run()
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
        fr_col = self.device_cols[d_col]
        device_view = view(fr_col)  # call constructor of view
        device_view.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        device.set_view(device_view)
        self.views.append(device_view)
        return device

    def cleanup(self):
        """Stops all devices."""
        for d in self.devices:
            try:
                d.stop()
            except Exception as e:
                print(e)
