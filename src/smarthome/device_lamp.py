import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView


class DeviceLampView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_power = tk.Label(self, text="Current Status:")
        self.l_power.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valpower = tk.Label(self, text="POWER_STATUS")
        self.l_valpower.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        if state["power"]:
            self.l_valpower.config(text="💡⚡")
        else:
            self.l_valpower.config(text="💡❌")


class DeviceLamp(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.state = {"power": False, "dim": 1.0}
        self._set_power_topic = self.get_base_path() + "set_power"
        self._set_dim_topic = self.get_base_path() + "set_dim"

    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_power_topic)
        self.mqtt_client.subscribe(self._set_dim_topic)

    def _client_message(self, client, userdata, msg):
        if self.on_message is not None:
            self.on_message(self, client, userdata, msg)
            return

        payload = self._decode_payload(msg.payload)

        if "value" not in payload:
            return

        if msg.topic == self._set_power_topic:
            self.set_power(payload["value"])
        elif msg.topic == self._set_dim_topic:
            self.set_dim(payload["value"])

    def set_power(self, power: bool):
        self._set_new_value("power", power)

    def set_dim(self, dim: float):
        dim = self.clamp(dim, 0.0, 1.0)
        self._set_new_value("dim", dim)
