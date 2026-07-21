"""
AI Robotics Bootcamp - Lesson 22
A tiny stand-in for ROS 2's `rclpy` library.

This exists so you can learn the REAL ROS 2 API before ROS 2 is installed.
It implements just enough of rclpy for the node code in ros2_style_demo.py
to be written exactly as it would be in a real ROS 2 package:

    Node.create_publisher(msg_type, topic, qos)
    Node.create_subscription(msg_type, topic, callback, qos)
    Node.create_timer(period, callback)
    Node.get_logger().info(...)
    rclpy.init() / rclpy.spin(...) / rclpy.shutdown()

It is NOT a real ROS 2 implementation - there is no networking, no DDS,
no separate processes. It only shows the shape of the API and how messages
flow between nodes.
"""


class String:
    """Stands in for std_msgs.msg.String."""

    def __init__(self, data=""):
        self.data = data

    def __repr__(self):
        return f"String(data={self.data!r})"


class _Logger:
    """Stands in for the ROS 2 logger, which prefixes the node name."""

    def __init__(self, node_name):
        self.node_name = node_name

    def info(self, message):
        print(f"[INFO] [{self.node_name}]: {message}")

    def warn(self, message):
        print(f"[WARN] [{self.node_name}]: {message}")


class _Publisher:
    def __init__(self, graph, topic, node_name):
        self.graph = graph
        self.topic = topic
        self.node_name = node_name

    def publish(self, msg):
        self.graph.deliver(self.topic, msg)


class Node:
    """Stands in for rclpy.node.Node."""

    def __init__(self, node_name):
        self._node_name = node_name
        self._logger = _Logger(node_name)
        self._timers = []
        _GRAPH.register(self)

    # --- the rclpy API ---------------------------------------------------
    def create_publisher(self, msg_type, topic, qos):
        return _Publisher(_GRAPH, topic, self._node_name)

    def create_subscription(self, msg_type, topic, callback, qos):
        _GRAPH.subscribe(topic, callback, self._node_name)
        return callback

    def create_timer(self, period_seconds, callback):
        self._timers.append((period_seconds, callback))
        return callback

    def get_logger(self):
        return self._logger

    def destroy_node(self):
        _GRAPH.unregister(self)


class _Graph:
    """Holds the topics and routes messages - the part ROS 2 normally does."""

    def __init__(self):
        self.subscriptions = {}     # topic -> [(node_name, callback)]
        self.nodes = []

    def register(self, node):
        self.nodes.append(node)

    def unregister(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def subscribe(self, topic, callback, node_name):
        self.subscriptions.setdefault(topic, []).append((node_name, callback))

    def deliver(self, topic, msg):
        for _node_name, callback in self.subscriptions.get(topic, []):
            callback(msg)

    def topics(self):
        return sorted(self.subscriptions.keys())

    def reset(self):
        self.subscriptions.clear()
        self.nodes.clear()


_GRAPH = _Graph()


class _Rclpy:
    """Stands in for the rclpy module itself."""

    @staticmethod
    def init(args=None):
        print("[rclpy] initialised (stand-in, not real ROS 2)\n")

    @staticmethod
    def spin(nodes, iterations=5):
        """Run every node's timers a number of times.

        Real rclpy.spin(node) blocks forever on ONE node. This version takes
        a list and runs a fixed number of cycles so the demo ends.
        """
        if not isinstance(nodes, list):
            nodes = [nodes]

        for _ in range(iterations):
            for node in nodes:
                for _period, callback in node._timers:
                    callback()

    @staticmethod
    def shutdown():
        print("\n[rclpy] shutdown")
        print(f"[rclpy] topics that existed: {', '.join(_GRAPH.topics())}")
        _GRAPH.reset()


rclpy = _Rclpy()
