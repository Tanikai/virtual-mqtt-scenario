# Setting up your MQTT scenario

!!! tip
    On this documentation page, code blocks can contain helpful annotations in form
    of a circular plus symbol:
    ``` Python
    # try clicking the (+) symbol! (1)
    ```

    1. This dialog contains additional information about the code.

If you want to set up your own MQTT scenario, you can use the `src/main.py`
file to add new devices. The most basic MQTT scenario without any devices can be
seen here:

```python
from application import App

config = { # (1)
    "host": "localhost",
    "port": 1883,
    "keepalive": 60,
}

app = App(config)
app.run() # Start GUI

# this part runs when the GUI is closed by the user
print("GUI was closed")
```

1. This dictionary is used to configure the connection to the MQTT broker. If
   you use a public one, be sure to edit the hostname and port. **Authentication with
   username and password is currently not supported.**

To add a new device, call the Constructor of the device and add it with `add_device`
to the application, as seen in the following code block:

```python
# ...
from device_thermometer import DeviceThermometer, DeviceThermometerView

t = DeviceThermometer(config, "my_house", "living_room", "thermometer") # what do the strings mean? (2)
app.add_device(t, DeviceThermometerView) # caution: (1)
```

1. When adding a device, be sure to pass a reference to the view class, **not a
   instance!** You can pass a class reference by typing the name of the class 
    **without parentheses ()**, for example DeviceThermometerView.
2. The strings are used in the MQTT Topic to describe in which house and room
   the device is located and how the device is called.

If you want to add multiple devices, you can create different variables to store
the devices or call the constructor directly in add_device:

``` Python
h_id = "my_house"
r_id = "living_room"

# create multiple devices in variables ...
w0 = DeviceWindow(config, h_id, r_id, "window0")
w1 = DeviceWindow(config, h_id, r_id, "window1")
app.add_device(w0, DeviceWindowView)
app.add_device(w1, DeviceWindowView)

# ... or add them directly
app.add_device(DeviceLamp(config, h_id, r_id, "lamp0"), DeviceLampView)
app.add_device(DeviceLamp(config, h_id, r_id, "lamp1"), DeviceLampView)
```

After you've added some devices to the scenario, sensor devices can publish data.
However, actuator devices are not able to react to published sensor data.
[Continue with the next guide to implement interactions between sensor and actuator devices.](extend-device.md)
