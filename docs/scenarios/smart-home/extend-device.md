# Implementing Device interactions

!!! tip
    On this documentation page, code blocks can contain helpful annotations in form
    of a circular plus symbol:
    ``` Python
    # try clicking the (+) symbol! (1)
    ```

    1. This dialog contains additional information about the code.

After adding some devices [as shown in the previous page](simulation-setup.md),
you can start implementing some interaction between them.

There are two main ways to add interactivity:

1. A sensor device publishes a message to the control topic of an actuator
   device (e.g. a remote control turns a lamp on).
2. . When a new
   message is published, the actuator decides if it wants to change its state.
   (e.g. a radiator turns itself on when the temperature is too low)

## Method 1: Publishing a Message to the Control Topic

In this code example, a sensor device publishes a message to the control topic
of an actuator device.

``` Python
home_id = "h0"
room_id = "living"
lamp = DeviceLamp(config, home_id, room_id, "ceiling_lamp")
app.add_device(lamp, DeviceLampView)

remote = DeviceRemote(config, home_id, room_id, "light_switch")
app.add_device(remote, DeviceRemoteView)

def _lamp_remote_clicked(self, input: str):
    self.mqtt_client.publish(f"{home_id}/{room_id}/ceiling_lamp/toggle_power", # (1)
                             "{}")
remote.on_click = _lamp_remote_clicked # (2)
remote.set_text("Toggle Light") # (3)
```

1. A String with a *f* prefix is called *f-string*. You can learn more about
   f-strings in [PEP 498](https://peps.python.org/pep-0498/).
2. When the Button in the View is clicked, the callback method that is assigned
   to on_click is called.
3. This is used to set a custom button text.

In this example, there are two devices:

1. A lamp that can be turned on or off. It has the
   topic `h0/living/ceiling_lamp`. It automatically subscribes
   to `h0/living/ceiling_lamp/set_power`
   and `h0/living/ceiling_lamp/toggle_power`.
   When a message is published to `set_power`, the contents have to be a JSON
   object (i.e. `{"power":True}`)

2. A remote control that has a Button in the GUI. When the button is clicked,
   the function `_lamp_remote_clicked` is called. The function publishes an
   empty JSON object to `h0/living/ceiling_lamp/toggle_power` to toggle the
   power status of the lamp.

## Method 2: Subscribing to Sensor Data

In this example, an actuator device subscribes to a topic of a sensor device.

``` Python
home_id = "h0"
room_id = "bathroom"

thermometer = DeviceThermometer(config, home_id, room_id, "thermometer")
app.add_device(thermometer, DeviceThermometerView)
        
window = DeviceWindow(config, home_id, room_id, "window")
app.add_device(window, DeviceWindowView)

def window_subscribe(self): 
    self.mqtt_client.subscribe(f"{home_id}/{room_id}/thermometer/humidity")
window.on_run = window_subscribe # (1)

def window_on_message(self, client, userdata, msg) -> bool:
    handled = False
    payload = self._decode_payload(msg.payload) # (2)
    if msg.topic == f"{home_id}/{room_id}/thermometer/humidity": # (3)
        humidity = float(payload["humidity"])
        if humidity > 60:  # alternatively: set_opened(humidity > 60)
            self.set_opened(True)
        else:
            self.set_opened(False)
        handled = True
    return handled # (4)

window.on_message = window_on_message
```

1. on_run is called after a connection to the MQTT broker has been established.
   This can be used to subscribe to custom topics. When window_subscribe is
   called, the device subscribes to the humidity readings of the thermometer.
2. By calling _decode_payload, the bytes of the PUBLISH Control Packet are
   converted to a Python dict.
3. window_on_message is called for every PUBLISH Control Packet the device
   receives. This means that you have to check if the Topic is 
4. The device has other topics that have to be checked, like the `set_opened`
   topic to open/close the window. If the PUBLISH Control Packet has been
   handled by your custom functionality, return `false` to stop further
   processing.

In this example, the Window device subscribes to the humidity readings of the
Thermometer. If the humidity exceeds 60%, the window opens automatically.

## Remote Control with user input

If you want to create a Remote Control Device with user input, here is an
example:

``` Python
radiator = DeviceRadiator(c, home_id, room_id, "towel_radiator")
app.add_device(radiator, DeviceRadiatorView)

r = DeviceRemote(c, home_id, room_id, "radiator_control", with_input=True) # (1)

def _bathroom_radiator_control_clicked(self, input: str):
  try:
      new_radiator_temp = float(input) # (2)
  except Exception as e:
      print("user input is not float:", e) # (3)
      return

  self.mqtt_client.publish(
      f"{home_id}/{room_id}/towel_radiator/set_temperature",
      json.dumps({"value": new_radiator_temp}))

r.on_click = _bathroom_radiator_control_clicked
app.add_device(r, DeviceRemoteView)
r.set_text("Set Radiator Temp")
```

1. To show a user input field in the Remote Control GUI, set the
   argument `with_input` to True.
2. Convert the string input to float for the control message
3. This is the most basic form exception handling. This can be extended to show
   a dialog message to the user with tkinter.

## Exercises

Here are some exercises if you want to experiment with interactions between
devices:

1. Create a remote control where the user can set a specific position for a
   Window Blind Device (possible values are between 0.0 and 1.0).
2. Create a lamp that automatically turns itself on between 17:00 and 21:00.
3. Create multiple windows and synchronize their `opened` status by making them
   controllable via a single topic.
