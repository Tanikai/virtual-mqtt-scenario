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
        self.tv_topics.bind("<<TreeviewSelect>>", self._on_topic_selected)
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

    def _on_topic_selected(self, event):
        if self.on_topic_selected is None:
            return
        # selection() returns a tuple with 1 element
        self.on_topic_selected(self.tv_topics.selection()[0])


class Explorer:
    """
    topic_path:
        children:
            topic_path: ...
            topic_path: ...
        messages: []
        tv_iid: string  # treeview identifier
    """

    def __init__(self, server_info: dict):
        self.conn_info = server_info
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.topictree = {
            "root": True,
            "name": "",
            "topic": "",
            "children": {},
            "messages": [],
        }
        self.view = None

    def run(self):
        self.mqtt_client.connect(self.conn_info["host"],
                                 self.conn_info["port"],
                                 self.conn_info["keepalive"])
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.mqtt_client.subscribe("#")

    def on_message(self, client, userdata, msg):
        self.insert_message(msg.topic, str(msg.payload.decode("utf-8")))

    def set_view(self, view: ExplorerView):
        self.view = view
        self.view.on_topic_selected = self.on_topic_selected

    def insert_message(self, topic: str, payload: str):
        """
        Inserts a new message into the topic tree.
        :param topic: Topic under which the message was published
        :param payload: Message of the PUBLISH Control Packet
        :return: None
        """
        node = self.get_topic_node(topic)
        self.add_message(node, payload)

    def get_topic_node(self, topic: str) -> dict:
        """
        Returns a topic tree node by topic.
        :param topic:
        :return: Node that corresponds to the topic.
        """
        if topic == "[empty]":
            return self.topictree["children"][""]

        topic_tokens = topic.split("/")
        node = self.topictree

        for token in topic_tokens:
            node = self.get_child(node, token)
        return node

    def get_child(self, node, child_name) -> dict:
        """
        Gets the child topic of a parent topic. If the specified child topic
        doesn't exist, a new node is created.
        :param node: Parent node
        :param child_name: Name of the child
        :return: Dictionary/Child Node
        """
        if "children" not in node:
            node["children"] = {}

        children = node["children"]
        # if child dictionary does not contain key child_name: create new
        if child_name not in children:
            if "root" in node:  # if parent node is root node: do not append /
                new_topic_id = child_name
            else:
                new_topic_id = f"{node['topic']}/{child_name}"
            children[child_name] = self.new_node(child_name, new_topic_id)
            # child_name is view_text, then current_topic as id
            view_id = children[child_name]["topic"]
            if view_id == "":  # if view id is empty:
                view_id = "[empty]"

            parent_view_id = node["topic"]
            if ("root" not in node) and (parent_view_id == ""):
                parent_view_id = "[empty]"

            self.add_node_to_view(child_name, view_id, parent_view_id)

        return children[child_name]

    @staticmethod
    def new_node(name, topic) -> dict:
        """
        Creates a new empty node for the topic tree.
        :param name: Name of the new node.
        :param topic: Topic that corresponds to this node
        :return: Newly created topic tree node.
        """
        return {
            "name": name,
            "topic": topic,
            "children": {},
            "messages": [],
        }

    def add_node_to_view(self, text: str, current_topic: str,
                         parent_topic: str):
        """
        Adds a new tkinter view to the topic tree hierarchy
        :param text: Text that is shown to the user for the topic token.
        :param current_topic: Token of the topic
        :param parent_topic: Parent topic
        :return: None
        """
        """"""
        if self.view is None:
            return
        tree = self.view.tv_topics
        tree.insert(parent_topic, tk.END, text=text, iid=current_topic,
                    open=True)

    def add_message(self, node: dict, message: str):
        """
        Adds a new message to the node and refreshes the message count of the
        view.
        :param node: Tree node of topic where the message was published.
        :param message: Message that was published.
        :return:
        """
        node["messages"].append(message)

        if self.view is None:
            return
        tree = self.view.tv_topics
        tree.item(node["topic"],
                  text=f"{node['name']} (Count: {len(node['messages'])})")

    def on_topic_selected(self, topic: str):
        """Callback method when a topic is clicked on by the user."""
        node = self.get_topic_node(topic)
        self.view.set_messages(node["messages"])
