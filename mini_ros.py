"""
AI Robotics Bootcamp - Lesson 17
A tiny ROS 2 style system, written from scratch.

ROS 2 itself is a large install, but its core idea is small enough to build
in one file. This shows the real architecture:

    Nodes publish messages to TOPICS.
    Nodes subscribe to TOPICS.
    No node ever calls another node directly.

That last line is the whole point. The camera node has never heard of the
motor node, yet an image ends up moving the robot.

Run with:
    python3 mini_ros.py
"""


# ---------------------------------------------------------------------------
# The message bus - this is the part ROS 2 normally provides for you
# ---------------------------------------------------------------------------

class Broker:
    """Routes messages from publishers to subscribers, by topic name."""

    def __init__(self):
        self.subscribers = {}       # topic name -> list of callback functions
        self.log = []

    def subscribe(self, topic, node_name, callback):
        self.subscribers.setdefault(topic, []).append((node_name, callback))
        print(f"  [{node_name}] subscribed to {topic}")

    def publish(self, topic, message, from_node):
        self.log.append((from_node, topic))
        listeners = self.subscribers.get(topic, [])

        if not listeners:
            # Publishing to a topic nobody listens to is not an error.
            # This is why a robot keeps running when one node dies.
            print(f"  {from_node} -> {topic}: (no subscribers)")
            return

        for node_name, callback in listeners:
            print(f"  {from_node} -> {topic} -> {node_name}")
            callback(message)


# ---------------------------------------------------------------------------
# Nodes - each does exactly one job
# ---------------------------------------------------------------------------

class Node:
    """Base class: every node has a name and access to the broker."""

    def __init__(self, name, broker):
        self.name = name
        self.broker = broker

    def publish(self, topic, message):
        self.broker.publish(topic, message, self.name)

    def subscribe(self, topic, callback):
        self.broker.subscribe(topic, self.name, callback)


class CameraNode(Node):
    """Only produces images. Knows nothing about AI or motors."""

    def __init__(self, broker, frames):
        super().__init__("camera_node", broker)
        self.frames = frames

    def capture(self, index):
        frame = self.frames[index % len(self.frames)]
        self.publish("/camera/image", frame)


class VisionNode(Node):
    """Turns an image into detections. Knows nothing about motors."""

    def __init__(self, broker):
        super().__init__("vision_node", broker)
        self.subscribe("/camera/image", self.on_image)

    def on_image(self, frame):
        # A real node would run YOLO here. We use the frame's contents.
        detections = [(label, conf) for label, conf in frame]
        self.publish("/detections", detections)


class BrainNode(Node):
    """Decides what to do. Knows nothing about cameras or wheels."""

    THRESHOLD = 0.80

    def __init__(self, broker):
        super().__init__("brain_node", broker)
        self.subscribe("/detections", self.on_detections)

    def on_detections(self, detections):
        confident = [name for name, conf in detections
                     if conf >= self.THRESHOLD]

        if "person" in confident:
            action = "STOP"           # safety first, as in Lesson 10
        elif "bottle" in confident:
            action = "APPROACH"
        else:
            action = "SEARCH"

        self.publish("/robot/action", action)


class MotorNode(Node):
    """Only drives wheels. Knows nothing about why."""

    def __init__(self, broker):
        super().__init__("motor_node", broker)
        self.subscribe("/robot/action", self.on_action)

    def on_action(self, action):
        wheels = {
            "STOP": "wheels stopped",
            "APPROACH": "driving forward",
            "SEARCH": "turning to look around",
        }
        print(f"      => {wheels.get(action, 'idle')}")


# ---------------------------------------------------------------------------

FRAMES = [
    [("chair", 0.94)],                      # nothing important
    [("bottle", 0.96), ("chair", 0.91)],    # something to fetch
    [("person", 0.99), ("bottle", 0.95)],   # a human appears
]


def main():
    print("=" * 62)
    print("  Lesson 17 - Nodes and topics")
    print("=" * 62)
    print("\nStarting nodes:\n")

    broker = Broker()
    camera = CameraNode(broker, FRAMES)
    VisionNode(broker)
    BrainNode(broker)
    MotorNode(broker)

    print("\n" + "-" * 62)
    print("Running the robot")
    print("-" * 62)

    for i in range(len(FRAMES)):
        print(f"\nframe {i + 1}: {FRAMES[i]}")
        camera.capture(i)

    # ---- Why this design matters ---------------------------------------
    print("\n" + "=" * 62)
    print("  What happens if the vision node crashes?")
    print("=" * 62 + "\n")

    broker.subscribers["/camera/image"] = []      # vision node is gone
    print("  vision_node removed.\n")
    camera.capture(0)
    print("\n  The camera kept publishing and did not crash. The rest of the")
    print("  robot is untouched. In one big program, that failure would have")
    print("  taken everything down. THIS is why robots are built from nodes.")


if __name__ == "__main__":
    main()
