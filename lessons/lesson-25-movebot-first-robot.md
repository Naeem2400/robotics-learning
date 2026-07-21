# Lesson 25 — Your First Robot in Webots

**Project 1 — MoveBot**

> Everything so far was foundation. From here we program robots the way a
> professional robotics engineer does.

---

## 🎯 Lesson Goal

- Understand the Webots interface
- Load a robot
- Write a Python controller
- Drive the robot forward
- Turn left and right

And see **your own robot moving on screen**.

---

## 🖥️ 1. The Webots Interface

```text
+--------------------------------------------+
|  Menu / Toolbar                            |
|                                            |
|  3D World          |   Text Editor         |
|    🤖 Robot        |                       |
|                                            |
|  Scene Tree        |   Console             |
+--------------------------------------------+
```

| Panel | What it is |
|---|---|
| **3D view** | Where the robot runs |
| **Scene Tree** | Every part of the robot — motors, sensors, camera |
| **Console** | Errors, warnings, and your `print()` output |

---

## 📁 2. Project Structure

A Webots project always has this shape:

```text
MoveBot/
├── controllers/
│   └── movebot_controller/
│       └── movebot_controller.py
└── worlds/
    └── movebot.wbt
```

> **The naming rule matters:** the controller folder name must **exactly**
> match the Python file name. `movebot_controller/movebot_controller.py` works;
> `movebot/controller.py` does not, and Webots fails silently.

**This repository is already a Webots project**, so MoveBot is ready to run:

```bash
open -a Webots worlds/movebot.wbt
```

Then press **▶ Run**.

---

## 🤖 3. Why the e-puck?

It is Webots' most popular beginner robot, and it already contains:

```text
e-puck
├── Camera
├── Left motor
├── Right motor
├── Distance sensors
└── LEDs
```

Nothing to assemble — you can focus on the code.

---

## 💻 4. The Code, Line by Line

### Create the robot object

```python
from controller import Robot

robot = Robot()
TIME_STEP = 64
```

`TIME_STEP = 64` means the simulation updates every **64 milliseconds**.

### Get the motors

```python
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
```

### Enable continuous rotation

```python
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
```

**This line confuses everyone, so understand it properly.** A motor has two
modes. By default it is in *position* mode — tell it `1.57` and it rotates to
that angle and stops, like a steering servo. Setting the position to
**infinity** switches it to *velocity* mode: "never stop turning, just spin at
the speed I give you." Wheels need velocity mode.

Forget this line and the wheels will not move, with no error message.

### Set the speed

```python
left_motor.setVelocity(4)
right_motor.setVelocity(4)
```

Speed is in **radians per second**, not metres per second.

### The control loop

```python
while robot.step(TIME_STEP) != -1:
    pass
```

This is robotics' **control loop**. Every robot has one running continuously.
`robot.step()` advances the simulation; it returns `-1` when Webots stops.

---

## 🎮 5. Movement Cheat Sheet

| Movement | Left | Right | Why |
|---|---|---|---|
| **Forward** | `4` | `4` | Both wheels equal |
| **Left turn** | `2` | `6` | Left wheel slower → curves left |
| **Right turn** | `6` | `2` | Right wheel slower → curves right |
| **Spin in place** | `-4` | `4` | Opposite directions |
| **Stop** | `0` | `0` | |

**One rule explains all five:** the robot turns *toward* the slower wheel.
Once that clicks, you never need to memorise the table.

---

## 🧪 6. Homework — Solved and Runnable

The homework asks for:

```text
5 seconds forward → left turn → 5 seconds forward → stop
```

That is implemented in
[`controllers/movebot_controller/movebot_controller.py`](../controllers/movebot_controller/movebot_controller.py):

```python
SEQUENCE = [
    ("Forward",   5.0,  SPEED,       SPEED),
    ("Left turn", 1.6,  SPEED * 0.5, SPEED * 1.5),
    ("Forward",   5.0,  SPEED,       SPEED),
    ("Stop",      0.0,  0.0,         0.0),
]
```

Console output:

```text
[ 0.00s] Forward
[ 5.00s] Left turn
[ 6.60s] Forward
[11.60s] Stop
Sequence complete. MoveBot stopped.
```

**Try changing the numbers.** Make the turn 3.2 seconds instead of 1.6 — the
robot turns roughly twice as far. Make it drive a square.

### What this teaches — and its limitation

This is **time-based control**: the robot has no idea where it is. It only
knows how long it has been doing something. Change the floor friction, the
battery level, or the robot's weight, and the same code produces a different
path.

Real robots therefore use **sensors** to close the loop — which is exactly
what Lesson 26 adds.

---

## 🏗️ 7. Architecture

```text
Python code → motor commands → Webots physics engine → robot movement
```

The same concept later applies to real hardware:

| Simulation | Real robot |
|---|---|
| `setVelocity(4)` | Motor driver → PWM signal → DC motor → wheel turns |

Same concept, different hardware. That is why simulation transfers.

---

## ⚠️ 8. Common Errors

| Error | Cause |
|---|---|
| Robot does not move | Forgot `setPosition(float("inf"))` |
| `getDevice` returns None | Wrong motor name — check the Scene Tree |
| Robot freezes | The control loop was removed |
| Controller never runs | Folder name ≠ file name |
| Nothing in the console | Wrong controller selected on the robot |

---

## 🎯 9. Interview Question

**Why use `setPosition(float("inf"))`?**

> To enable continuous wheel rotation. If you set a specific position, the
> motor only rotates to that position and stops.

<details>
<summary>Follow-up: why is speed in rad/s instead of m/s?</summary>

Because the motor turns a *wheel*, and a motor's natural unit is angular
velocity. Converting to ground speed requires the wheel radius:
`speed = angular_velocity × radius`. The e-puck's wheels are about 2 cm in
radius, so 4 rad/s ≈ 0.08 m/s. Two robots given the same rad/s but different
wheel sizes travel at different speeds — a real source of bugs when porting
code between robots.
</details>

---

## 💡 10. 2026 Industry Note

In modern autonomous robots motor commands are not set by hand:

```text
Camera → AI vision → Path planner → ROS 2 controller → Motor controller → Robot
```

Motor control receives its commands from AI and planning systems. You are
writing the last box in that chain; the rest of the course fills in the ones
before it.

---

## 🚀 Next — Lesson 26: Obstacle Avoidance

Your first **autonomous** robot:

```text
Distance sensor → obstacle detected → decision → turn → keep moving
```

This closes the loop that time-based control leaves open.

> We built exactly this in Lesson 10 with the TurtleBot
> ([`worlds/turtlebot_room.wbt`](../worlds/turtlebot_room.wbt)). Lesson 26 can
> bring that logic onto MoveBot's e-puck and its distance sensors.

---

## ⭐ Course Note — Where Simulation Goes Next

Webots is excellent for learning. Later, **NVIDIA Isaac Sim / Isaac Lab**
becomes relevant for reinforcement learning, humanoid training, and Jetson
deployment — used by NVIDIA, Figure AI, Unitree, and Agility Robotics.

Webots is the right choice now. Moving to Isaac later is straightforward
because the concepts — worlds, robots, controllers, sensors, control loops —
are identical.
