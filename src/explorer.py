import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt


class Explorer(tk.Frame):
    tv_topics = None  # topic tree
    mqtt_client = mqtt.Client()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.tv_topics = ttk.Treeview(self)  # self (Frame) as master
        self.tv_topics.pack(fill=tk.BOTH, expand=True)

    def run(self):
        try:
            self.mqtt_client.connect()
        except ConnectionError as e:
            print("Connection Error to broker:", e)
            return

        self.mqtt_client.loop_start()