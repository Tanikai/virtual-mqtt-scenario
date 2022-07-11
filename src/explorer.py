import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt


class ExplorerView(tk.Frame):
    tv_topics = None  # topic tree

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.tv_topics = ttk.Treeview(self)  # self (Frame) as master
        self.tv_topics.heading('#0', text='MQTT Explorer Topics', anchor=tk.W)
        self.tv_topics.insert('', tk.END, text="/", iid="/")  # iid is topic
        self.tv_topics.pack(fill=tk.BOTH, expand=True)


class Explorer:
    mqtt_client = mqtt.Client()
    view = None

    topictree = {
        "topic": "/",
        "children": {},
        "messages": [],
    }

    """
    topic_path:
        children:
            topic_path: ...
            topic_path: ...
        messages: []
        tv_iid: string  # treeview identifier
    """

    def __init__(self, ):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def run(self):
        try:
            self.mqtt_client.connect("localhost", 1883, 60)
        except ConnectionError as e:
            print("Connection Error to broker:", e)
            return

        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        # self.insert_message(msg.topic, str(msg.payload.decode("utf-8")))
        print(msg.topic + " " + str(msg.payload))

    def set_view(self, view: ExplorerView):
        self.view = view

    def insert_message(self, topic: str, payload: str):
        topic_tokens = topic.split("/")
        topic_tokens.pop(0)
        node = self.topictree

        for token in topic_tokens:
            node = self.get_child(node, token)
        node["messages"].append(payload)
        print(self.topictree)

    def get_child(self, node, child_name) -> dict:
        if "children" not in node:
            node["children"] = {}

        children = node["children"]
        if child_name not in children:
            children[child_name] = self.new_node(node["topic"] + "/" + child_name)
            self.add_node_to_view(child_name, children[child_name]["topic"], node["topic"])

        return children[child_name]

    def new_node(self, topic) -> dict:
        return {"topic": topic, "children": {}, "messages": []}

    def add_node_to_view(self, text: str, current_topic: str, parent_topic: str, ):
        if self.view is None:
            return
        tree = self.view.tv_topics
        tree.insert(parent_topic, tk.END, text=text, iid=current_topic)
