# Create your own Device

!!! tip
    On this documentation page, code blocks can contain helpful annotations in form
    of a circular plus symbol:
    ``` Python
    # try clicking the (+) symbol! (1)
    ```

    1. This dialog contains additional information about the code.

If you have an idea for a new Device, you can use this page as a reference.
Additionally, reading the source code of already implemented Device can be
helpful for you.

## Tkinter Reference

This project uses tkinter for the frontend. Here are some references for tkinter
components:

- [Official Python3 Docs: Graphical User Interfaces with Tk](https://docs.python.org/3/library/tk.html)
- [Official Python3 Docs: Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html)
- [Official Python3 Docs: Tk themed widgets](https://docs.python.org/3/library/tkinter.ttk.html)
- [Tkinter 8.5 reference: a GUI for Python (last updated in 2013, unmaintained)](https://tkdocs.com/shipman/)

## Creating the view class

```Python
class DeviceLampView(DeviceBaseView): # (1)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_device.config(text="Lamp", background=self.actuator_color)
        # add Labels to show data (2)
        self.l_power = tk.Label(self, text="Current Status:")
        self.l_power.grid(row=self.row_offset, column=0, sticky=tk.W) # (3)
        self.l_valpower = tk.Label(self, text="POWER_STATUS")
        self.l_valpower.grid(row=self.row_offset, column=1, sticky=tk.W)

    def set_state(self, state: dict): # (4)
        super().set_state(state) # (5)
        if state["power"]: # (6)
            self.l_valpower.config(text="Turned ON", background="green")
        else:
            self.l_valpower.config(text="Turned OFF", background="red")
```

1. All View classes for Devices inherit from `DeviceBaseView`. DeviceBaseView
   inherits from tkinter.Frame, which represents a container, similar to `<div>`
   in HTML.
2. The Lamp View uses tkinter Labels to show its current status. They are
   aligned inside the Frame with `.grid()`.
3. Because there are already multiple rows added by DeviceBaseView,
   use `self.row_offset` to use the next free row. Specify the column of the
   Label with the `column` argument.
4. `set_state` is called when the Device Controller sets a new state for the
   view. Based on the contents of the state, the view decides how to represent
   the information.
5. Before handling the Device-specific view, `set_state` of the parent class
   should be called for general view handling.
6. The state is passed as a dict with key-value-pairs. In this example, the text
   is set to different texts based on the boolean-value of `"power"`.

When you create a new View class for a Device, you can use the `DeviceBaseView`
class as a parent.

## Implementing the data generator

You can skip this step if you want to create an Actuator Device.

If you want to generate different data for a Sensor Device, you need to
implement a generator first. The following example shows a data generator that
alternates between the values "A" and "B". As the data generator has to operate
independently of the Device controller / MQTT Client, `GeneratorBase` inherits
from `threading.Thread`.

``` Python
class CustomGenerator(GeneratorBase):
    def __init__(self, callback):
        super().__init__(callback) # (1)
        self.current_value = "A"

    def run(self):
        while not self.event.is_set(): # (2)
            self.callback({"my_value": self.current_value) # (3)
            self.event.wait(5) # (4)
            
    def change_value(self):
        if self.current_value == "A":
            self.current_value = "B"
        else:
            self.current_value = "A"
```

1. Be sure to call the super constructor to set the callback event.
2. This while-loop runs until the threading.Event instance is set. The event
   object is used to communicate to the thread that it should stop.
3. This is used to pass data back to the Device controller.
4. In order to stop during the waiting period, `event.wait()` is used instead
   of `sleep()`. When `sleep()` is used, the cancel condition can only be
   checked after the waiting period has passed. By using `event.wait()`, the
   thread can be stopped immediately.

## Implementing the Device controller

### Actuator Devices

As Actuator Devices don't have a generator, the controller is very simple.

``` Python
class DeviceLamp(DeviceBase):

    def __init__(self, server_info: dict, home_id: str, room_id: str,
                 device_id: str):
        super().__init__(server_info, home_id, room_id, device_id) # (1)
        self.state = {"power": False} # (2)
        # Private string variables for topics
        self._power_topic = self.get_base_path() + "power"
        self._set_power_topic = self.get_base_path() + "set_power"
        self._toggle_power_topic = self.get_base_path() + "toggle_power"

    # override subscribe_controls method to subscribe to control topics
    def subscribe_controls(self):
        self.mqtt_client.subscribe(self._set_power_topic)
        self.mqtt_client.subscribe(self._toggle_power_topic)

    # override _client_message method to create
    def _client_message(self, client, userdata, msg):
        handled = super()._client_message(client, userdata, msg) # (3)
        if handled:
            return

        payload = self._decode_payload(msg.payload) # (4)

        if msg.topic == self._toggle_power_topic:
            self.set_power(not self.state["power"])
        if msg.topic == self._set_power_topic:
            self.set_power(payload["value"])

    # change the state of the device
    def set_power(self, power: bool):
        if self.state["power"] is not power: # (5)
            self.mqtt_client.publish(self._power_topic, json.dumps({"power": power}))
        self._set_new_value("power", power)

```

1. Be sure to call the super constructor of DeviceBase.
2. This is the initial state of the device.
3. Here, the _client_message method of DeviceBase is called to check for a
   custom on_message handler that has been set during configuration
   (i.e. `mydevice.on_message = callback_func`). If the custom callback_func
   already handled the message, the default _client_message method exits.
4. The payload has to be converted from a byte array to a UTF8-String.
5. The device only publishes a message when the state is changed. For example,
   when the initial state is `power = False` and `set_power(True)` is called two
   times, only one MQTT message is published.

### Sensor Devices

Sensor devices are a bit more complicated as they have a data generator.

``` Python
class DeviceClock(DeviceBase):

    def __init__(self, server_info, home_id, device_id):
        super().__init__(server_info, home_id, "", device_id) # (1)
        self.generator = ClockGenerator(self._on_new_data) # (2)
        self.state = {"time": "12:00"}

    # override get_base_path to remove the room topic.
    def get_base_path(self) -> str:
        return f"{self.home_id}/{self.device_id}/"

    def _on_new_data(self, data: dict):
        handled = super()._on_new_data(data)
        if handled:
            return

        self.mqtt_client.publish(self.get_base_path() + "time",
                                 json.dumps({"time": data["time"]}))
        self._new_state(data) # (3)
```

1. The Clock Device is a house-specific device without a room topic. Therefore,
   an empty string is passed for the `room_id` argument.
2. The `self.generator` attribute is used for the generator. In the `run()`
   method of DeviceBase, `self.generator` is started automatically if it is
   not `None`. Additionally, the callback method for new data is set
   to `self._on_new_data`.
3. To update the Device's state and its view, `self._new_state(data)` has to be
   called with the new data from the generator.

## Further Questions

If you have further questions that haven't been answered by the previous guide
pages, you can check out the sample devices found
in `src/smarthome/device_***.py`.