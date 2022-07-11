from application import App
from smarthome.device_thermostat import DeviceThermostat, DeviceThermostatView

if __name__ == '__main__':
    app = App()

    # create new instance of DeviceThermostat, but only pass constructor
    app.add_device(DeviceThermostat(), DeviceThermostatView)
    app.run()
