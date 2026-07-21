"""
AI Robotics Bootcamp - Lesson 22
Your first ROS 2 program - written in real ROS 2 style, runnable today.

ROS 2 is not installed on this machine yet, so the bottom half of this file
provides a tiny stand-in for `rclpy` (ROS 2's Python library).

The important part: THE NODE CODE ABOVE IS WRITTEN EXACTLY AS REAL ROS 2
CODE. When you run ROS 2 in Docker later, you delete the shim and change
one line:

    from mini_rclpy import Node, rclpy      ->      import rclpy
                                                    from rclpy.node import Node

Everything else stays the same.

Run with:
    python3 ros2_style_demo.py
"""

from mini_rclpy import Node, rclpy, String


# ===========================================================================
# REAL ROS 2 STYLE CODE - this is what you would write in a ROS 2 package
# ===========================================================================

class TalkerNode(Node):
    """Publishes a message on a timer. The classic ROS 2 'talker'."""

    def __init__(self):
        super().__init__("talker")
        self.publisher = self.create_publisher(String, "chatter", 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f"Hello robot: {self.count}"
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.publisher.publish(msg)
        self.count += 1


class ListenerNode(Node):
    """Subscribes to the same topic. The classic ROS 2 'listener'."""

    def __init__(self):
        super().__init__("listener")
        self.subscription = self.create_subscription(
            String, "chatter", self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


class MotorNode(Node):
    """A third node, to show that many nodes can share one topic."""

    def __init__(self):
        super().__init__("motor")
        self.subscription = self.create_subscription(
            String, "chatter", self.on_command, 10)

    def on_command(self, msg):
        if msg.data.endswith(("0", "2", "4", "6", "8")):
            self.get_logger().info("   motors: driving forward")
        else:
            self.get_logger().info("   motors: turning")


def main():
    rclpy.init()

    talker = TalkerNode()
    listener = ListenerNode()
    motor = MotorNode()

    # In real ROS 2 each node usually runs in its OWN terminal, started with
    # `ros2 run`. Here we spin them together so you can watch the exchange.
    rclpy.spin([talker, listener, motor], iterations=5)

    talker.destroy_node()
    listener.destroy_node()
    motor.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
