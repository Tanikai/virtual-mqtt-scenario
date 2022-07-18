import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from typing import List


class ExplorerView(tk.Frame):
    tv_topics = None  # topic tree
    on_topic_selected = None

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        # self (Frame) as master
        # selectmode=browse: only one selection allowed
        self.tv_topics = ttk.Treeview(self, selectmode='browse')
        self.tv_topics.heading("#0", text="MQTT Explorer Topics", anchor=tk.W)
        self.tv_topics.insert("", tk.END, text="/", iid="/",
                              open=True)  # iid is topic
        self.tv_topics.bind("<<TreeviewSelect>>", self.__on_topic_selected)
        self.tv_topics.pack(fill=tk.BOTH, expand=True)
        self.lb_messages = tk.Listbox(self, height=16)
        self.lb_messages.pack(side=tk.BOTTOM, fill=tk.X)
        self.l_messages = tk.Label(self, text="Messages:")
        self.l_messages.pack(side=tk.BOTTOM, anchor=tk.NW)

    def set_messages(self, messages: List[str]):
        self.lb_messages.delete(0, tk.END)
        # Explanation: asterisk before messages is "splat" operator, found as
        # "Unpacking Argument Lists" in the documentation
        # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
        self.lb_messages.insert(tk.END, *messages)

    def add_message(self, message: str):
        self.lb_messages.insert(tk.END, message)

    def __on_topic_selected(self, event):
        if self.on_topic_selected is None:
            return
        # selection() returns a tuple with 1 element
        self.on_topic_selected(self.tv_topics.selection()[0])


class Explorer:
    mqtt_client = mqtt.Client()
    view = None

    topictree = {
        "name": "",
        "topic": "",
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
        self.insert_message(msg.topic, str(msg.payload.decode("utf-8")))

    def set_view(self, view: ExplorerView):
        self.view = view
        self.view.on_topic_selected = self.on_topic_selected

    def insert_message(self, topic: str, payload: str):
        node = self.get_topic_node(topic)
        self.add_message(node, payload)

    def get_topic_node(self, topic: str) -> dict:
        if topic == "/":
            return self.topictree

        topic_tokens = topic.split("/")
        topic_tokens.pop(0)
        node = self.topictree

        for token in topic_tokens:
            node = self.get_child(node, token)
        return node

    def get_child(self, node, child_name) -> dict:
        if "children" not in node:
            node["children"] = {}

        children = node["children"]
        if child_name not in children:
            children[child_name] = self.new_node(
                child_name, f"{node['topic']}/{child_name}")
            self.add_node_to_view(child_name, children[child_name]["topic"],
                                  node["topic"])

        return children[child_name]

    def new_node(self, name, topic) -> dict:
        return {
            "name": name,
            "topic": topic,
            "children": {},
            "messages": [],
        }

    def add_node_to_view(self, text: str, current_topic: str,
                         parent_topic: str, ):
        if self.view is None:
            return
        tree = self.view.tv_topics
        tree.insert(parent_topic, tk.END, text=text, iid=current_topic,
                    open=True, )

    def add_message(self, node: dict, message: str):
        node["messages"].append(message)

        if self.view is None:
            return
        tree = self.view.tv_topics
        tree.item(node["topic"],
                  text=f"{node['name']} (Count: {len(node['messages'])})")

    def on_topic_selected(self, topic: str):
        node = self.get_topic_node(topic)
        self.view.set_messages(node["messages"])
