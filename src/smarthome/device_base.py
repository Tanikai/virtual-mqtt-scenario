import paho.mqtt.client as mqtt
from tkinter import Frame, Label


class DeviceBaseView(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = Label(parent, text="Hello World!")
        self.label.pack()

    def set_state(self, state: dict):
        self.label.config(text=state["device_topic"])


class DeviceBase:
    mqtt_client = mqtt.Client()

    home_id: str
    room_id: str
    device_id: str

    state: dict  # general object for storing state

    view = None

    def __init__(self):
        self.home_id = "0"
        self.room_id = "test"
        self.device_id = "deviceBase"
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def __del__(self):
        self.mqtt_client.loop_stop()

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
        client.subscribe("#")

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


