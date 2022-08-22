import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView
from src import tools


class DeviceLampView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Lamp", background=self.actuator_color)
        self.l_power = tk.Label(self, text="Current Status:")
        self.l_power.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valpower = tk.Label(self, text="POWER_STATUS")
        self.l_valpower.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        if state["power"]:
            self.l_valpower.config(text="Turned ON", background="green")
        else:
            self.l_valpower.config(text="Turned OFF", background="red")


class DeviceLamp(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.state = {"power": False}
        self._power_topic = self.get_base_path() + "power"
        self._set_power_topic = self.get_base_path() + "set_power"
        self._toggle_power_topic = self.get_base_path() + "toggle_power"

    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_power_topic)
        self.mqtt_client.subscribe(self._toggle_power_topic)

    def _client_message(self, client, userdata, msg):
        handled = super()._client_message(client, userdata, msg)
        if handled:
            return

        payload = self._decode_payload(msg.payload)

        if msg.topic == self._toggle_power_topic:
            self.set_power(not self.state["power"])

        if msg.topic == self._set_power_topic:
            self.set_power(payload["value"])

    def set_power(self, power: bool):
        if self.state["power"] is not power:
            self.mqtt_client.publish(self._power_topic,
                                     json.dumps({"power": power}))
        self._set_new_value("power", power)
