# Lesson 9 — Robot Simulation

**Module 5 — Development Environment & Simulation**

---

## First, a Question

### What is simulation?

A **simulation** is a virtual version of the real world — an artificial world
built inside a computer.

Think of a racing game. The car is not real. The road is not real. The physics
is calculated by the computer. That is a simulation.

Robotics works exactly the same way.

---

## Real World Examples

Tesla does **not** put a new car straight onto a public road:

```text
Simulation  →  Testing  →  Thousands of runs  →  Real car
```

Boston Dynamics and Figure AI follow the same path — simulation first, then
the physical robot.

This is why **simulation is the industry standard.** There are three concrete
reasons:

| Reason | Why it matters |
|---|---|
| **Cost** | A crashed virtual robot costs nothing. A crashed real one costs thousands. |
| **Speed** | You can run a test 500 times overnight, faster than real time. |
| **Safety** | Bugs that would injure someone stay harmless inside the computer. |

---

## Which Software Will We Use?

### ⭐ Webots

Webots is an excellent simulator for beginner and intermediate robotics. In it
you can build:

- Robot car
- Humanoid robot
- Drone
- Robot arm
- Mobile robot

...and control all of them with Python.

### Why Webots?

| | |
|---|---|
| ✅ | Free and open source |
| ✅ | Python support |
| ✅ | ROS 2 integration |
| ✅ | Runs natively on Apple Silicon |
| ✅ | Used professionally |

---

## What Happens Inside a Simulation?

```text
Virtual World
      ↓
    Robot
      ↓
Virtual Camera
      ↓
Virtual LiDAR
      ↓
Virtual Motors
      ↓
 Python Code
      ↓
 Robot Moves
```

The key insight: **you get sensors and motors without owning any hardware.**
The Python code you write against a virtual LiDAR is nearly identical to the
code you would write against a real one.

---

## The Webots Interface

```text
+----------------------------------+
| 3D World                         |
|                                  |
|        🤖 Robot                  |
|                                  |
+----------------------------------+

Scene Tree          Console
```

### The three main components

**1. World** — your virtual environment: a room, a road, a maze, a factory.

**2. Robot** — the virtual robot, which may carry wheels, a camera, LiDAR,
GPS, a compass, or an IMU.

**3. Controller** — a Python program. This is the robot's brain.

---

## The Robot's Flow

```text
Camera  →  Python  →  Decision  →  Motors  →  Movement
```

Exactly like a real robot — and exactly the same sense→decide→act loop from
Module 4.

---

## Our First Simulation

We will use a simple robot and a simple sequence:

```text
Forward  →  Stop  →  Turn left  →  Forward
```

No AI yet. Just movement. Walk before running.

The code is in this repository at
[`controllers/first_robot/first_robot.py`](../controllers/first_robot/first_robot.py).

---

## Industry Knowledge

A professional robotics engineer works in this order:

```text
1. Build the robot model
2. Add sensors
3. Write the code
4. Test in simulation
5. Fix bugs
6. Deploy to the real robot
```

Steps 4 and 5 repeat many times before step 6 ever happens. That is why
simulation matters so much.

---

## Installation

### Step 1 — Download

Get the latest stable release from the official site:
**https://cyberbotics.com**

On macOS you can also install it with Homebrew (already installed on your
machine):

```bash
brew install --cask webots
```

### Step 2 — Open Webots

You will find a set of sample worlds included.

### Step 3 — Press Run

The robot will move on its own. **Do not write any code yet** — just observe.
Watch how the world, the robot, and the console relate to each other.

### Step 4 — Verify

```bash
python3 setup_check.py
```

Webots should now show as `[x]`.

---

## Running Your Own Controller

This repository **is** a Webots project, so there is nothing to copy:

```text
Robotics/
├── worlds/
│   └── first_robot.wbt          ← the virtual world
└── controllers/
    └── first_robot/
        └── first_robot.py       ← the robot's brain
```

Just open the world and press Run:

```bash
open -a Webots worlds/first_robot.wbt
```

The world already has the e-puck's `controller` field set to `first_robot`,
so Webots finds the Python file automatically.

> **Note on Webots conventions:** a controller must live in a folder whose
> name matches the Python file exactly —
> `controllers/first_robot/first_robot.py`. If the names differ, Webots will
> not find it. The same applies to the `worlds/` and `controllers/` folder
> names: Webots looks for those exact names at the project root.

### First-run notes on macOS

- **"System below the minimal requirements"** — expected on Apple Silicon.
  Webots only recognises discrete NVIDIA/AMD cards, so it disables shadows and
  anti-aliasing. This affects appearance only, never physics or sensors.
- **Gatekeeper blocks the app** — Cyberbotics does not notarise their macOS
  builds. Right-click the app in Finder → **Open** → **Open** to approve it
  once. Double-clicking gives you no Open button.

---

## Homework

1. Install Webots.
2. Open it.
3. Run a sample world.
4. Report back:
   - Did Webots open successfully?
   - Did the sample robot move?

---

## 🎯 Interview Questions

Questions you should be able to answer after this lesson:

1. Why do robotics companies test in simulation before using real hardware?
2. What is the difference between a *world* and a *controller* in Webots?
3. What is the "reality gap", and why does code that works in simulation
   sometimes fail on a real robot?

<details>
<summary>Answer to #3</summary>

The **reality gap** is the difference between simulated and real physics.
Simulators approximate friction, sensor noise, motor lag, and lighting. A
controller tuned to perfect simulated sensors often fails on a real robot
whose readings are noisy. Engineers narrow the gap by adding artificial noise
to simulations and by testing on hardware early.
</details>

---

## ⚡ Common Mistakes

- **Controller folder name does not match the file name** — Webots silently
  fails to load it.
- **Forgetting `setPosition(float('inf'))`** — without it, the motor is in
  position mode and `setVelocity` will not spin the wheel continuously.
- **Ignoring the simulation timestep** — every controller needs a
  `while robot.step(timestep) != -1:` loop, or nothing advances.
- **Testing only in a perfect world** — add obstacles and noise early.

---

## 🚀 Next

With simulation running, the next module begins the portfolio projects — the
first being an **obstacle-avoidance robot** that uses the distance sensors we
have only read about so far.
