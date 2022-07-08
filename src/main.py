import threading
import time
from tkinter import *
#from smarthome.device_base import DeviceBase
from smarthome.device_thermostat import DeviceThermostat

label = None

def mythread():
    time.sleep(2)
    label.config(text="changed")
    print("changed now")

if __name__ == '__main__':
    #d = DeviceBase()
    d = DeviceThermostat()
    d.run()

    root = Tk()
    root.geometry('800x600')
    label = Label(root, text="Hello World!")
    #
    # t = threading.Thread(target=mythread)
    # t.start()
    #
    label.pack()
    root.mainloop()

    d.stop()


