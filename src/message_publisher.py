import tkinter as tk
import paho.mqtt.client as mqtt


class MessagePublisherView(tk.Frame):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(borderwidth=2, relief="groove")
        self.l_title = tk.Label(self, text="Publish Message", anchor=tk.W)
        self.l_title.pack(side=tk.TOP, fill=tk.X)
        self.l_topic = tk.Label(self, text="Topic:", anchor=tk.W)
        self.l_topic.pack(side=tk.TOP, fill=tk.X)
        self.e_topic = tk.Entry(self)
        self.e_topic.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.l_message = tk.Label(self, text="Message:", anchor=tk.W)
        self.l_message.pack(side=tk.TOP, fill=tk.X)
        self.e_message = tk.Entry(self)
        self.e_message.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.bt_send = tk.Button(self, text="Send Message",
                                 command=self._send_message)
        self.bt_send.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.on_send_message = None

    def _send_message(self):
        if self.on_send_message is None:
            return

        topic = self.e_topic.get()
        if topic == "":
            return
        msg = self.e_message.get()

        self.on_send_message(topic, msg)


class MessagePublisher:

    def __init__(self, server_info: dict):
        self.conn_info = server_info
        self.mqtt_client = mqtt.Client()

        self.view = None

    def run(self):
        self.mqtt_client.connect(self.conn_info["host"],
                                 self.conn_info["port"],
                                 self.conn_info["keepalive"])
        self.mqtt_client.loop_start()

    def set_view(self, view: MessagePublisherView):
        self.view = view
        self.view.on_send_message = self.publish_message

    def publish_message(self, topic, msg):
        self.mqtt_client.publish(topic, msg)
