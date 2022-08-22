# List of Smart Home Devices

## General

Every device can be assigned to a house and room. Some devices are only
assignable to a whole house.

| Attribute | Description                          |
|-----------|--------------------------------------|
| house_id  | The house the device is assigned to. |
| room_id   | The room the device is assigned to.  |
| device_id | The device's own id.                 |

The house, room and device IDs are used in the topic structure like this:

house/room/device_id/

Example: house_0/living_room/temperature_sensor0/

For every sensor, there are Data (Publisher) and Control (Subscriber) Topics.
Control Topics are subscribed to automatically by the device.

!!! important

    MQTT Topics should not start with a leading slash "/" (Example: /house0/light).
    When you do this, the part before the slash is treated as a topic name,
    which means that the first topic name is an empty string.

## Room-specific devices

### Thermometer

This is a classic temperature and humidity sensor for indoor usage.

Data:

| **Relative Topic** | **Type** | **Description**                   |
|--------------------|----------|-----------------------------------|
| ./temperature      | Float    | New temperature reading (Celsius) |
| ./humidity         | Float    | New humidity reading              |

Ranges for Data:

- Temperature: -100.0 - 100.0
- Humidity: 0.0 - 1.0

Controls: none

---

### Window Blinds

This device simulates window blinds that can be rolled up or down.

Data:

| **Relative Topic** | **Type** | **Description**           |
|--------------------|----------|---------------------------|
| ./position         | Float    | New window blind position |

Ranges for Data:

- opened / float (0.0-1.0) / current status

Controls:

| **Relative Topic** | **Type** | **Description**                |
|--------------------|----------|--------------------------------|
| ./set_position     | Float    | Set position for window blinds |

---

### Radiator Controls

This device simulates a radiator knob that can be set to different target
temperatures.

Data:

| **Relative Topic** | **Type** | **Description**                    |
|--------------------|----------|------------------------------------|
| ./temperature      | Float    | New target temperature of radiator |

Controls:

| **Relative Topic** | **Type** | **Description**              |
|--------------------|----------|------------------------------|
| ./set_temperature  | Float    | Set a new target temperature |

---

### Window

This device simulates a window sensor that can detect whether a window is
opened or closed.

Data:

| **Relative Topic** | **Type** | **Description**   |
|--------------------|----------|-------------------|
| ./opened           | Boolean  | New window status |

Controls:

| **Relative Topic** | **Type** | **Description**      |
|--------------------|----------|----------------------|
| ./set_opened       | Boolean  | Open or close window |
| ./toggle_opened    | None     | Toggle window state  |

---

### Smart Lights

This device simulates a light source. It can be turned on/off and dimmed.

Data:

| **Relative Topic** | **Type** | **Description**           |
|--------------------|----------|---------------------------|
| ./power            | Boolean  | New power status of light |


Controls:

| **Relative Topic** | **Type** | **Description**      |
|--------------------|----------|----------------------|
| ./set_power        | Boolean  | Turn light on or off |
| ./toggle_power     | None     | Toggle power state   |

---

### (Light) Button

This device simulates a button. It can be used for example as a light switch or
window opener/closer.

Data:

| **Relative Topic** | **Type** | **Description**                     |
|--------------------|----------|-------------------------------------|
| ./pressed          | None     | Is published when button is pressed |

Controls: none

---

## House-specific devices

### Weather Sensor

This sensor simulates weather changes. It also measures the outside temperature.

Data:

| **Relative Topic**    | **Type** | **Description**         |
|-----------------------|----------|-------------------------|
| ./weather             | Text     | New weather status      |

Ranges for Data:

- Weather: clear / cloudy / rain

Controls: none

---

### Clock

This device broadcasts the current time of day. In this scenario, one real-time
second equals 5 virtual minutes. The frequency of time events can be changed by
setting the interval. For example, when it is set to 20, a new event is
published every 20 virtual minutes (or 4 real seconds).

Data:

| **Relative Topic** | **Type**       | **Description**       |
|--------------------|----------------|-----------------------|
| ./time             | String (HH:MM) | New time event        |

Controls: None
