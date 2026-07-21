# Lesson 10 — The Robot's Brain (Decision Making)

**Module 5 — Professional Development Environment**

> Today you learn to think like a robot.

This lesson is the foundation of AI, robotics, ROS 2, and autonomous systems.

---

## ❌ The Mistake 90% of Courses Make

They jump straight into Webots, ROS 2, or Gazebo. The result: students
copy-paste code but never understand **how a robot actually thinks**. So before
Lesson 11, we fix that.

---

## Real World Example

Imagine you are walking through a room. Your eyes see a chair. Your brain says:

```text
"There is a chair."  →  "Do not bump into it."  →  "Go around the left."
```

You made that decision automatically. A robot does exactly the same thing:

```text
Camera  →  Image  →  Brain  →  Decision  →  Motor  →  Move
```

That is the core of robotics.

---

## The Robot Decision Cycle

Every robot in the world — Tesla, Boston Dynamics, Figure AI, Unitree, a drone,
a warehouse robot — follows the same cycle:

```text
Sense  →  Think  →  Act  →  (repeat)
```

This is called the **Sense → Think → Act loop**.

### Step 1 — Sense

The robot collects information through its sensors: camera, LiDAR, ultrasonic,
GPS, IMU, temperature sensor, microphone. These are the robot's eyes and ears.

### Step 2 — Think

The robot decides what to do with that information:

```python
if distance < 20:
    stop()
```

*The wall is close, so stop.*

### Step 3 — Act

A command goes to the motors: stop, turn left, move, pick object, open gripper.

### Step 4 — Repeat

A robot does not decide once. It runs this loop many times per second —
20, 50, 100, sometimes 1000 times. It is a **continuous loop**.

```text
Camera → Detect human → Measure distance → Human safe? → No → Brake → Check again → …
```

---

## Robot Memory and State

A robot also remembers things. If `battery = 15%`, it thinks *"charge is low"*
and starts looking for a charging station.

**State** means *what the robot is doing right now*:

```text
Moving   Stopped   Charging   Searching   Picking   Avoiding obstacle   Talking
```

These states define the robot's behaviour.

---

## Finite State Machine (FSM)

Professional robots organise those states into a **Finite State Machine** — the
robot is always in exactly one state, and rules move it from one to the next.

```text
START → SEARCH OBJECT → (object found?) → YES → MOVE → PICK → RETURN → END
```

FSMs are extremely common in ROS 2 and industrial robotics.

```python
robot_state = "SEARCH"

if robot_state == "SEARCH":
    print("Looking for object")
elif robot_state == "MOVE":
    print("Moving to object")
elif robot_state == "PICK":
    print("Picking object")
```

This same logic later becomes ROS 2 nodes.

---

## Real Examples

**Warehouse robot** picking a box — every step is a state:

```text
Receive mission → Find shelf → Go to shelf → Box found? → Pick box → Deliver → Return
```

**Humanoid robot** hearing *"Bring me water"*:

```text
Voice → Speech recognition → Understand command → Find bottle → Walk →
Pick bottle → Return → Give bottle
```

This combines AI, robotics, vision, and planning all at once.

---

## Industry Architecture

Almost every advanced robot has this pipeline:

```text
Sensors → Perception → Planning → Decision → Controller → Motors → Movement
```

---

## Software Engineer vs Robotics Engineer

| Software Engineer | Robotics Engineer |
|---|---|
| `Input → Output` | `Sensor → Decision → Movement → new Sensor → new Decision → …` |

A normal program runs once and stops. A robot lives in a loop with the physical
world. That is what makes robotics different.

---

## Mini Project — `robot_brain.py`

The runnable version is in this repository:
[`robot_brain.py`](../robot_brain.py).

```python
battery = 25
distance = 15

if battery < 20:
    print("Go to charging station")
elif distance < 20:
    print("Obstacle detected")
    print("Turn left")
else:
    print("Move forward")
```

Change the values and observe:

| Input | Output |
|---|---|
| `battery = 10`, `distance = 100` | `Go to charging station` |
| `battery = 80`, `distance = 10` | `Obstacle detected` / `Turn left` |

---

## Industry Challenge

A robot has this data:

```python
battery = 50
distance = 12
human_detected = True
```

What should the robot do? Write the logic yourself before reading on.

<details>
<summary>How to think about it</summary>

The key idea is **priority**. When several conditions are true at once, safety
comes first:

1. **Human safety** — a detected human always wins. Stop immediately.
2. **Battery** — if too low to finish, go charge.
3. **Obstacle** — avoid it.
4. Otherwise, move forward.

With the data above, `human_detected` is `True`, so the robot **stops** — even
though the battery is fine and the obstacle rule would otherwise fire. The order
in which you check the rules *is* the robot's set of priorities. This is solved
in [`robot_brain.py`](../robot_brain.py).
</details>

---

## Homework

1. Create `robot_brain.py`.
2. Test different `battery` and `distance` values.
3. Add a new rule: if `human_detected = True`, the robot stops.

---

## 🎯 Next — Lesson 11 (very important)

**Object-Oriented Programming (OOP) for Robotics** — the turning point of the
course. You will learn what a class and an object are, and build a `Robot`
class, plus `Sensor`, `Motor`, `Camera`, `LiDAR`, and `RobotBrain` classes.
From there we start building **professional robotics software architecture**.

> **Suggestion:** since your goal is AI engineering + robotics + freelancing,
> push your code to GitHub after every lesson. In 6–8 months you will have not
> just notes but a **professional robotics portfolio** to show clients and
> employers. (This repository already does that. ✅)
