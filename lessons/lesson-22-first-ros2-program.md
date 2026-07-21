# Lesson 22 — Your First ROS 2 Program

**Module 13 — ROS 2 Practical**

> Lesson 17 explained nodes and topics. Now you write them in **real ROS 2
> code**.

---

## 🎯 Lesson Goal

- What a ROS 2 workspace and package are
- How to write a publisher node
- How to write a subscriber node
- The `rclpy` API you will use for years
- How to run it before ROS 2 is installed

---

## 📖 1. ROS 2 Project Structure

Real ROS 2 code lives in a **workspace** containing **packages**:

```text
ros2_ws/                        the workspace
├── src/
│   └── my_robot/               a package
│       ├── package.xml         package metadata
│       ├── setup.py            build instructions
│       └── my_robot/
│           ├── talker.py       a node
│           └── listener.py     a node
├── build/                      generated
├── install/                    generated
└── log/                        generated
```

Commands you will use:

```bash
mkdir -p ros2_ws/src && cd ros2_ws
ros2 pkg create --build-type ament_python my_robot   # create a package
colcon build                                          # build the workspace
source install/setup.bash                             # make it available
ros2 run my_robot talker                              # run a node
```

---

## 💻 2. A Publisher Node (real ROS 2 code)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TalkerNode(Node):
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
```

Line by line:

| Code | Meaning |
|---|---|
| `class TalkerNode(Node)` | Every node is a class inheriting from `Node` — **this is the OOP from Lesson 11** |
| `super().__init__("talker")` | Registers the node's name with ROS 2 |
| `create_publisher(String, "chatter", 10)` | Publish `String` messages on the `chatter` topic; `10` is the queue depth |
| `create_timer(1.0, cb)` | Call `cb` once per second |
| `get_logger().info(...)` | ROS 2's logging, not `print()` |

## A Subscriber Node

```python
class ListenerNode(Node):
    def __init__(self):
        super().__init__("listener")
        self.subscription = self.create_subscription(
            String, "chatter", self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')
```

Note it is **callback-driven**: you never call `listener_callback` yourself.
ROS 2 calls it whenever a message arrives.

---

## 🔬 3. Practical — Run It Now

ROS 2 is not installed yet (see Lesson 21), so this course ships a small
stand-in for `rclpy`:

```bash
python3 ros2_style_demo.py
```

Output:

```text
[INFO] [talker]: Publishing: "Hello robot: 0"
[INFO] [listener]: I heard: "Hello robot: 0"
[INFO] [motor]:    motors: driving forward
[INFO] [talker]: Publishing: "Hello robot: 1"
[INFO] [listener]: I heard: "Hello robot: 1"
[INFO] [motor]:    motors: turning
```

**The node code in [`ros2_style_demo.py`](../ros2_style_demo.py) is written
exactly as real ROS 2 code.** Only the import line differs:

```python
# today
from mini_rclpy import Node, rclpy, String

# in a real ROS 2 container
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
```

Everything else — `create_publisher`, `create_subscription`, `create_timer`,
`get_logger`, `spin`, `destroy_node` — is the genuine API.

[`mini_rclpy.py`](../mini_rclpy.py) is the stand-in. It is worth reading: in
about 100 lines it shows what ROS 2 does for you — keeping a registry of
topics and routing messages to whoever subscribed.

> **⚠️ Be clear about what this is not.** The stand-in has no networking, no
> DDS, and no separate processes. Real ROS 2 nodes run as independent programs,
> often on different computers. This teaches the API and the message flow, not
> the distributed systems underneath.

---

## 🧩 4. Three Nodes, One Topic

The demo runs a **third** node — a motor node also subscribing to `chatter`.
Watch the output: one publisher, two subscribers, and the publisher knows about
neither.

This is the payoff of the topic model. Adding a logger, a recorder, or a safety
monitor requires **no change to the talker at all**.

---

## 🖥️ 5. Running Real ROS 2 (in Docker)

Once Docker is installed:

```bash
docker run -it ros:jazzy bash
source /opt/ros/jazzy/setup.bash
```

Terminal 1:

```bash
ros2 run demo_nodes_py talker
```

Terminal 2 (`docker exec -it <container> bash` first):

```bash
ros2 run demo_nodes_py listener
```

Useful inspection commands:

```bash
ros2 node list          # which nodes are running
ros2 topic list         # which topics exist
ros2 topic echo /chatter    # watch messages live
ros2 topic hz /chatter      # how fast are they arriving
```

`ros2 topic echo` is the single most useful debugging command in ROS 2. When
a robot misbehaves, the first question is always *"is the data actually
arriving?"*

---

## ⚠️ 6. Common Mistakes

- **Forgetting to `source install/setup.bash`** — then `ros2 run` cannot find
  your package. The most common beginner error by far.
- **Using `print()` instead of `get_logger()`** — you lose timestamps, node
  names, and log levels.
- **Mismatched topic names.** `/chatter` and `chatter` differ; a typo means the
  subscriber silently receives nothing. No error appears — this is why
  `ros2 topic list` matters.
- **Mismatched message types.** A publisher sending `String` and a subscriber
  expecting `Int32` will not connect.
- **Forgetting `rclpy.init()`**.

---

## 🎯 7. Interview Questions

**Q: What is the difference between a node and a topic?**

> A node is a program that does one job. A topic is a named channel that nodes
> publish messages to and subscribe to.

<details>
<summary>Q: What does the number 10 mean in create_publisher(String, "chatter", 10)?</summary>

It is the **queue size** (part of the Quality of Service settings). If the
publisher produces messages faster than a subscriber consumes them, up to 10
are buffered before the oldest are dropped. Small queues suit real-time sensor
data where a stale reading is useless; larger queues suit data you must not
lose.
</details>

---

## 🚀 Next — Lesson 23: Professional Development Environment

Folder structure, VS Code extensions, virtual environments, and the project
scaffolding you will reuse for every project from here on.
