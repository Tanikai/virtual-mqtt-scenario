import paho.mqtt.client as mqtt
import tkinter as tk
import typing
import json
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
    sensor_color = "medium purple"
    actuator_color = "orange"
    """
    This is the base class for the Device View.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.row_offset = 3
        # General Config
        self.config(borderwidth=2, relief="groove")
        self.l_device = tk.Label(self, text="device_not_specified", padx=5)
        self.l_device.grid(row=0, column=0, sticky=tk.W)
        # Topic Info
        self.l_topic = tk.Label(self, text="Topic:")
        self.l_topic.grid(row=1, column=0, sticky=tk.W)
        self.l_valtopic = tk.Label(self, text="DEVICE_TOPIC")
        self.l_valtopic.grid(row=1, column=1, sticky=tk.W)
        # Last Refresh Info
        self.l_lastchange = tk.Label(self, text="Last Change:")
        self.l_lastchange.grid(row=2, column=0, sticky=tk.W)
        self.l_vallastchange = tk.Label(self, text="LAST_CHANGE")
        self.l_vallastchange.grid(row=2, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        self.l_valtopic.config(text=state["device_topic"])
        self.l_vallastchange.config(text=datetime.now().strftime("%H:%M:%S"))


class DeviceBase:
    """
    This is the base class for all devices in the scenario.
    """

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        self.conn_info = server_info
        self.mqtt_client = mqtt.Client()

        self.generator = None
        self.state = {}
        self.view = None

        # Custom functions
        self.on_new_data = None
        """Edit data from generator before passing it to the device."""

        self.on_new_state = None
        self.on_run = None  # subscribe to custom topics here
        self.on_connect = None
        self.on_message = None  # react to custom messages here
        self._on_subscribe_controls = None

        self.home_id = home_id
        self.room_id = room_id
        self.device_id = device_id
        self.mqtt_client.on_connect = self._client_connect
        self.mqtt_client.on_message = self._client_message

    def set_view(self, view: DeviceBaseView):
        """Sets the tkinter frontend for the object."""
        self.view = view

    def run(self):
        """Connect to the MQTT Broker and start generating data"""
        self.mqtt_client.connect(self.conn_info["host"],
                                 self.conn_info["port"],
                                 self.conn_info["keepalive"])
        self.subscribe_controls()  # subscribe to control topics
        if self.on_run is not None:
            self.on_run(self)
        if self.generator is not None:
            # run is blocking, start is non-blocking
            self.generator.start()

        self._new_state(self.state)

        self.mqtt_client.loop_start()

    def stop(self):
        if self.generator is not None:
            self.generator.event.set()

    def get_base_path(self) -> str:
        """returns the base path of the MQTT topic for the device"""
        return f"{self.home_id}/{self.room_id}/{self.device_id}/"

    def _client_connect(self, client, userdata, flags, rc):
        if self.on_connect is not None:
            self.on_connect(self, client, userdata, flags, rc)
            return

    def subscribe_controls(self):
        """
        Subscribes to topics that are used to control a device.
        Override this method in child classes if a device should have controls.
        :return:
        """
        pass

    def _client_message(self, client, userdata, msg):
        """Callback method when a PUBLISH Control Packet is received from the
        server."""
        if self.on_message is not None:
            handled = self.on_message(self, client, userdata, msg)
            return handled
        else:
            return False # not handled

    def _on_new_data(self, data: dict) -> bool:
        if self.on_new_data is not None:
            handled = self.on_new_data(self, data)
            return handled
        else:
            return False

    def _new_state(self, state: dict):
        self.state = state
        self.state["device_topic"] = self.get_base_path()

        self._state_changed()

    def _state_changed(self):
        if self.on_new_state is not None:
            self.on_new_state(self)

        if self.view is not None:
            self.view.set_state(self.state)

    @staticmethod
    def _decode_payload(payload) -> dict:
        try:
            payload_str = str(payload.decode("utf-8"))
            return json.loads(payload_str)
        except Exception as e:
            print("An Error occurred while decoding the json", e)
            return {}

    def _set_new_value(self, key: str, value: any):
        self.state[key] = value
        self._state_changed()
