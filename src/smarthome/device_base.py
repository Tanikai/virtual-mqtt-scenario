import paho.mqtt.client as mqtt
import tkinter as tk
from datetime import datetime


class DeviceBaseView(tk.Frame):
    roff = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        # General Config
        self.config(borderwidth=2, relief="groove")
        # Topic Info
        self.l_topic = tk.Label(self, text="Topic:")
        self.l_topic.grid(row=0, column=0, sticky=tk.W)
        self.l_valtopic = tk.Label(self, text="DEVICE_TOPIC")
        self.l_valtopic.grid(row=0, column=1, sticky=tk.W)
        # Last Refresh Info
        self.l_lastrefresh = tk.Label(self, text="Last Refresh:")
        self.l_lastrefresh.grid(row=1, column=0, sticky=tk.W)
        self.l_vallastrefresh = tk.Label(self, text="LAST_REFRESH")
        self.l_vallastrefresh.grid(row=1, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        self.l_valtopic.config(text=state["device_topic"])
        self.l_vallastrefresh.config(text=datetime.now().strftime("%H:%M:%S"))


class DeviceBase:
    mqtt_client = mqtt.Client()

    home_id = "DEFAULT_HOME_ID"
    room_id = "DEFAULT_ROOM_ID"
    device_id = "DEFAULT_DEVICE_ID"

    state: dict  # general object for storing state

    view = None

    def __init__(self):
        self.home_id = "0"
        self.room_id = "test"
        self.device_id = "deviceBase"
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message


    def run(self):
        try:
            self.mqtt_client.connect("localhost", 1883, 60)
        except ConnectionError as e:
            print("Connection Error to broker:", e)
            return

        self.mqtt_client.loop_start()

    def get_base_path(self):
        return f"/{self.home_id}/{self.room_id}/{self.device_id}/"

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        #client.subscribe("#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def set_view(self, view: DeviceBaseView):
        self.view = view

    def new_state(self, state: dict):
        if self.view is None:
            return
        state["device_topic"] = self.get_base_path()
        self.view.set_state(state)
