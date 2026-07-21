# Lesson 17 — ROS 2: The Backbone of Every Professional Robot

**Module 10 — ROS 2 (Robot Operating System 2)**

> **Golden rule:** ROS 2 is **not** an operating system. It is a software
> framework and communication platform for robotics.

> 💡 **Important correction:** the name misleads people into thinking ROS is
> like Windows or macOS. It is not. ROS 2 is robotics **middleware** that runs
> *on top of* Ubuntu, macOS, or another OS.

---

## 🎯 Lesson Goal

After this lesson you will understand:

- What ROS 2 is and why it was created
- Why every robot needs something like it
- What nodes and topics are
- What publishers and subscribers are

---

## 📖 1. Theory — The Problem ROS 2 Solves

Picture a simple robot with a camera, LiDAR, motors, a battery, an AI model,
and a voice system. **How do they all talk to each other?**

### Without ROS 2

```text
Camera  ─┐
LiDAR   ─┼──→ one giant AI program ──→ Motors
Battery ─┘
```

Every component wires directly into every other component. With 10 components
that is up to 45 separate connections. Change one, and you risk breaking the
rest. This does not scale.

### With ROS 2

Every component does its own job, and **ROS 2 handles all communication**:

```text
Camera ─┐
LiDAR  ─┤
GPS    ─┼──→  ROS 2  ──→  AI Brain  ──→  Motors
IMU    ─┤
Voice  ─┘
```

### The hospital analogy

A hospital has reception, doctors, pharmacy, laboratory, and billing. Each
department does its own work, and they do **not** all phone each other
directly — there is a system for passing information around. ROS 2 plays that
role inside a robot.

---

## 🧩 2. Node

### Definition

A **node** is an independent program that performs one specific job.

Think of dividing the robot into small workers, each doing only its own task:

| Node | Job |
|---|---|
| Camera node | Only sends images |
| LiDAR node | Only sends distances |
| Motor node | Only controls motors |
| Voice node | Only speaks |

```text
Robot
├── Camera Node
├── LiDAR Node
├── Navigation Node
├── Voice Node
├── Battery Node
└── Motor Node
```

Each node is independent.

---

## 📡 3. Topic

If nodes are separate programs, how do they talk? Through **topics**.

### The group chat analogy

A WhatsApp group called "Family" — everyone posts messages there, and everyone
in the group receives them. Nobody messages each other individually.

In ROS 2 that group is a **topic**:

```text
/camera/image
```

The camera node **publishes** images to it. The AI node **subscribes** and
receives them.

| Term | Meaning |
|---|---|
| **Publisher** | A node that sends messages |
| **Subscriber** | A node that receives messages |

### The complete flow

```text
Camera Node → publishes → /camera/image → AI Node
   → processes → decision → /robot/action → Motor Node → robot moves
```

---

## 💻 4. Practical — Build It Yourself

ROS 2 is a large install, but its core idea fits in one file. Run this:

```bash
python3 mini_ros.py
```

[`mini_ros.py`](../mini_ros.py) is a working publish/subscribe system with four
real nodes — camera, vision, brain, motor:

```text
frame 2: [('bottle', 0.96), ('chair', 0.91)]
  camera_node -> /camera/image -> vision_node
  vision_node -> /detections   -> brain_node
  brain_node  -> /robot/action -> motor_node
      => driving forward
```

### The key thing to notice

**The camera node has never heard of the motor node.** There is no line of code
connecting them. Yet an image ends up moving the robot, because each node only
knows about *topics*, never about other nodes. That decoupling is the entire
idea behind ROS 2.

The script then **deletes the vision node mid-run** to show what happens:

```text
  camera_node -> /camera/image: (no subscribers)
```

The camera keeps publishing. Nothing crashes. In one big program, that failure
would have taken the whole robot down.

---

## 💪 5. Why Modularity Matters

If the camera breaks, the rest of the robot keeps running — because the parts
are separate nodes, not one tangled program.

### Industry examples

| Organisation | Modular design |
|---|---|
| **Boston Dynamics** | Separate systems for walking, balance, vision, mapping, navigation |
| **NASA rovers** | Software split into modules so one failure does not doom the mission |
| **Warehouse robots** | Barcode, navigation, battery, charging, fleet management nodes |

For a Mars rover, this is not a style preference — a single crash-prone program
would risk the entire mission with no possibility of repair.

---

## 🏗️ 6. ROS 2 Architecture

```text
     +----------------+
     | Camera Node    |
     +----------------+
             │
             ▼
      /camera/image
             │
     +------------------+
     | AI Vision Node   |
     +------------------+
             │
             ▼
      /robot/action
             │
     +------------------+
     | Motor Node       |
     +------------------+
             │
             ▼
        Robot moves
```

---

## ⚠️ 7. Common Mistakes

- **Thinking ROS 2 is only Python.** It supports Python *and* C++. Performance
  critical nodes are usually C++.
- **Thinking a robot is one program.** A professional robot may run dozens or
  hundreds of nodes.
- **Writing everything in one file.** That is not how industry builds robots —
  and you now know exactly why.
- **Thinking ROS 2 is an operating system.** It is middleware running on top of
  one.

---

## 🎯 8. Interview Questions

**Q: What is a node?**

> A node is an independent program in ROS 2 that performs one specific task,
> such as camera control, navigation, or motor control.

<details>
<summary>Q: Why use topics instead of letting nodes call each other directly?</summary>

Decoupling. A publisher does not know or care who is listening — there may be
zero subscribers, or five. That means you can add a data-logging node, swap the
camera for a different model, or restart a crashed node without touching any
other code. Direct calls would require every node to know about every other
node, which is exactly the tangle ROS 2 exists to prevent.
</details>

<details>
<summary>Q: What happens if a node crashes?</summary>

Only that node's function is lost — the others keep running, because they
communicate through topics rather than direct calls. This is why safety-critical
robots are built this way. A well-designed system also detects the missing data
and degrades safely, for example stopping when vision goes quiet rather than
driving blind.
</details>

---

## 🧠 Mini Quiz

A robot has a camera, LiDAR, YOLO AI, and a motor.
**Which are publishers and which are subscribers?**

```text
Camera → ????? → YOLO
```

<details>
<summary>Answer</summary>

Most nodes are **both**.

- **Camera** — publisher only (produces images, consumes nothing)
- **LiDAR** — publisher only
- **YOLO / vision** — *subscriber* to `/camera/image`, *publisher* to
  `/detections`
- **Motor** — subscriber only (consumes commands, produces nothing)

The pattern: sensors are pure publishers, actuators are pure subscribers, and
everything in between is both. Run `mini_ros.py` and you can watch exactly this
happen.
</details>

---

## 📌 9. 2026 Industry Note

ROS 2 is very popular, but not every company uses the identical stack:

- Research labs and universities use ROS 2 heavily
- Many startups build **custom software on top of** ROS 2
- High-performance systems combine ROS 2 with C++, CUDA, and AI frameworks
  such as the NVIDIA ecosystem

So ROS 2 is a **strong foundation**, but Python, Linux, and AI matter just as
much alongside it.

---

## 🛣️ Roadmap

```text
Robotics ✅   Electronics ✅   Programming ✅   Sensors ✅
Computer Vision ✅   YOLO ✅   ROS 2 basics ✅
```

The next phase is real robotics engineering.

---

## 🚀 Next — Lesson 18: Linux for Robotics

Essential, because:

- ROS 2's primary development environment is Linux
- The Jetson Orin Nano runs Linux
- Most professional robots are Ubuntu-based
- You will learn to manage files, permissions, and packages like an engineer

We will keep developing on your Mac, so that when you move to a Jetson the
transition is smooth.
