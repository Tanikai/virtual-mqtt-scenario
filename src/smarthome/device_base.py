import paho.mqtt.client as mqtt
import tkinter as tk
import typing
from datetime import datetime
from threading import Thread, Event


class GeneratorBase(Thread):
    """
    This class is the base class for all generator objects. Generator objects
    are used by sensor devices to generate data for the simulated scenario.
    It inherits from threading.Thread so that it doesn't block the single
    threaded Global Interpreter Lock of Python while waiting to generate
    the next value.
    """

    def __init__(self, callback: typing.Callable):
        """
        Constructor for the generator thread.
        :param callback: Callback function that is called when new data is
        generated.
        """
        super().__init__(daemon=True)
        self.callback = callback
        self.event = Event()  # for stopping generator

    def stop(self):
        """
        Stops the generator thread.
        :return:
        """
        self.event.set()


class DeviceBaseView(tk.Frame):
    """
    This is the base class for the Device View.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.row_offset = 2
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
    """
    This is the base class for all devices in the scenario.

    """

    def __init__(self):
        self.mqtt_client = mqtt.Client()

        self.generator = None
        self.state = {}
        self.view: DeviceBaseView

        # Custom functions
        self.on_new_data = None
        """Edit data from generator before passing it to the device."""

        self.on_new_state = None
        self.on_run = None  # subscribe to custom topics here
        self.on_connect = None
        self.on_message = None  # react to custom messages here
        
        self.home_id = "0"
        self.room_id = "test"
        self.device_id = "deviceBase"
        self.mqtt_client.on_connect = self._client_connect
        self.mqtt_client.on_message = self._client_message

    def set_view(self, view: DeviceBaseView):
        self.view = view

    def run(self):
        try:
            self.mqtt_client.connect("localhost", 1883, 60)
            if self.on_run is not None:
                self.on_run()
            if self.generator is not None:
                # run is blocking, start is non-blocking
                self.generator.start()

        except ConnectionError as e:
            print("Connection Error to broker:", e)
            return

        self.mqtt_client.loop_start()

    def stop(self):
        if self.generator is not None:
            self.generator.event.set()

    def get_base_path(self) -> str:
        return f"/{self.home_id}/{self.room_id}/{self.device_id}/"

    def _client_connect(self, client, userdata, flags, rc):
        if self.on_connect is not None:
            self.on_connect()
            return
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("#")

    # The callback for when a PUBLISH message is received from the server.
    def _client_message(self, client, userdata, msg):
        if self.on_message is not None:
            self.on_message(client, userdata, msg)
            return
        print(msg.topic + " " + str(msg.payload))

    def _on_new_data(self, data: dict) -> bool:
        if self.on_new_data is not None:
            self.on_new_data(data)
            return True
        else:
            return False

    def _new_state(self, state: dict):
        self.state = state
        self.state["device_topic"] = self.get_base_path()

        if self.on_new_state is not None:
            self.on_new_state()

        if self.view is None:
            return
        self.view.set_state(self.state)
