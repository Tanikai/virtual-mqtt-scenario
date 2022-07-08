import paho.mqtt.client as mqtt

class DeviceBase:
    mqtt_client = mqtt.Client()

    home_id: str
    room_id: str
    device_id: str

    #@property
    state: dict # general object for storing state

    def __init__(self):
        self.home_id = "0"
        self.room_id = "test"
        self.device_id = "deviceBase"
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("localhost", 1883, 60)

    def __del__(self):
        self.mqtt_client.loop_stop()

    def run(self):
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
