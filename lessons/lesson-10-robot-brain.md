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

## Running the Brain on a Real Simulated Robot

The terminal version uses numbers you type in. The simulation version reads
**real sensors** and drives **real motors** — the same brain, brought to life.

```bash
open -a Webots worlds/turtlebot_room.wbt   # then press Run
```

A small TurtleBot3 with a 360° lidar explores a large furnished room, turning
away from the sofa, fridge, cabinet, plants, and boxes. Its brain is
[`controllers/turtlebot_brain/turtlebot_brain.py`](../controllers/turtlebot_brain/turtlebot_brain.py),
a state machine with three states:

| State | Behaviour |
|---|---|
| `FORWARD` | Drive ahead until something is within 0.4 m |
| `TURN` | Rotate in place toward the more open side until the way is clear |
| `BACK` | If wedged, reverse and try turning the other way |

That `BACK` state matters: without an escape behaviour, any obstacle-avoiding
robot will eventually trap itself in a corner.

---

## ⚡ Two Real Problems We Hit (and what they teach)

These are not bugs we invented for the lesson — we hit them while building it.

### 1. The robot drove under a table and got stuck

A 2D lidar scans at **one fixed height**. On our first robot it sat about
30 cm off the floor, but a tabletop is ~74 cm high on thin legs:

```text
        ___________________  <- tabletop (the robot's BODY hits this)
       |                   |
   ····|···················|····  <- lidar beams scan here and see a GAP
      leg                 leg
```

The sensor honestly reported "clear" — it was looking *underneath* the
obstacle. The robot then wedged its body on something its eyes never saw.

**The lesson:** one sensor has blind spots. This is exactly why real
self-driving cars and warehouse robots combine cameras, radar, *and* lidar —
each covers what the others miss. Our fix was to use obstacles that reach the
floor, which the low lidar can actually see.

### 2. A big robot could not navigate a small room

Our first robot was human-sized with an arm sticking out. In a small room full
of furniture it had no room to manoeuvre, and its arm clipped objects that were
outside the sensor's forward cone. Swapping to a small robot with a smooth
round body and a 360° sensor fixed it instantly.

**The lesson:** the robot's **body shape and size** are part of the navigation
problem, not just the software. A wide robot needs wider gaps, larger safety
margins, and sensors that cover its whole footprint. Engineers call this the
robot's *footprint* and it is a real parameter in ROS 2 navigation.

> Both versions are kept in this repository so you can compare them: the large
> [TIAGo](../worlds/tiago_room.wbt) and the small
> [TurtleBot3](../worlds/turtlebot_room.wbt) run *the same brain* with very
> different results.

---

## Homework

1. Create `robot_brain.py`.
2. Test different `battery` and `distance` values.
3. Add a new rule: if `human_detected = True`, the robot stops.
4. Run the simulation and change `TURN_DISTANCE` in the controller. What
   happens if it is very small (0.15) or very large (1.5)?

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
