import json
import tkinter as tk
from .device_base import DeviceBase, DeviceBaseView
from src import tools


class DeviceRadiatorView(DeviceBaseView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Radiator", background=self.actuator_color)
        self.l_targettemp = tk.Label(self, text="Target Temperature:")
        self.l_targettemp.grid(row=self.row_offset, column=0, sticky=tk.W)
        self.l_valtargettemp = tk.Label(self, text="TARGET_TEMPERATURE")
        self.l_valtargettemp.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict):
        super().set_state(state)
        if "temperature" in state:
            self.l_valtargettemp.config(text=str(state["temperature"]))


class DeviceRadiator(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id)
        self.state = {"temperature": 20.0}
        self._temperature_topic = self.get_base_path() + "temperature"
        self._set_temperature_topic = self.get_base_path() + "set_temperature"

    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_temperature_topic)

    def _client_message(self, client, userdata, msg):
        if self.on_message is not None:
            handled = self.on_message(self, client, userdata, msg)
            if handled:
                return

        payload = self._decode_payload(msg.payload)

        if "value" not in payload:
            return

        if msg.topic == self._set_temperature_topic:
            self.set_temperature(payload["value"])

    def set_temperature(self, temperature: float):
        temperature = tools.clamp(temperature, 16.0, 28.0)
        if self.state["temperature"] != temperature:
            self.mqtt_client.publish(self._temperature_topic,
                                     json.dumps({"temperature": temperature}))
        self._set_new_value("temperature", temperature)
