import threading
import time
from tkinter import *

label = None

def mythread():
    time.sleep(2)
    label.config(text="changed")
    print("changed now")

if __name__ == '__main__':
    root = Tk()
    root.geometry('800x600')
    label = Label(root, text="Hello World!")

    t = threading.Thread(target=mythread)
    t.start()

    label.pack()
    root.mainloop()

