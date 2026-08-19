# Lesson 45 — First SLAM Robot Simulation

**Module 18 — SLAM & Autonomous Navigation**

> We are moving from theory to a **virtual robotics laboratory**. No hardware
> today. The MacBook runs Webots; Webots runs a TurtleBot3; the TurtleBot3
> carries a virtual LiDAR.

Lesson 44 explained SLAM. This lesson does **not** implement SLAM. It does
the measurement SLAM is made of: a robot moving, a laser returning metres,
a rule that says *stop*.

```text
MacBook
  ↓
Webots
  ↓
Virtual robot
  ↓
Virtual LiDAR
  ↓
Virtual hallway
  ↓
Movement + a decision
```

The same architecture later becomes ROS 2 + a real LiDAR + a Jetson. The
wiring does not change. The sensors become physical.

---

## 🎯 Lesson Goal

- What Webots is (and why we use it before buying a robot)
- World vs robot vs controller
- What a virtual LiDAR actually returns
- Drive forward, watch the wall approach, stop at **1 metre**
- Why this is **not** SLAM yet — and how it connects

**Do not install ROS 2 this lesson.**

---

## 📖 1. Webots Is a Virtual Lab

Webots is an open-source, cross-platform robotics simulator. It runs on
macOS (including Apple Silicon), Windows, and Linux. Controllers can be
Python, C/C++, Java, MATLAB, or ROS.

Official site: [cyberbotics.com](https://cyberbotics.com)

Documentation used for this lesson (R2025a, the version our `.wbt` files
already declare):

- [User Guide — sensors](https://cyberbotics.com/doc/guide/sensors?version=R2025a)
- [Reference — `Lidar` node](https://cyberbotics.com/doc/reference/lidar?version=R2025a)
- [Tutorials](https://cyberbotics.com/doc/guide/tutorials?version=R2025a)
  (Tutorial 1: first simulation, Tutorial 6: four-wheel robot)

In plain language: **a house you can crash a robot into for free.**

```text
Real robot    ❌  not today
Virtual robot ✅  this lesson
```

You already met Webots in [Lesson 9](lesson-09-robot-simulation.md) and drove
an e-puck in [Lesson 25](lesson-25-movebot-first-robot.md). Today the robot
is a **TurtleBot3 Burger** and the sensor is a **360° LiDAR**, because that
is what SLAM stacks actually subscribe to.

---

## 🖥️ 2. Install / Confirm Webots

Latest stable release: [cyberbotics.com](https://cyberbotics.com)

macOS shortcut (from Lesson 9):

```bash
brew install --cask webots
python3 setup_check.py          # Webots should show [x]
```

Gatekeeper: Cyberbotics does not notarise the Mac build. Right-click
**Webots.app → Open → Open** the first time.

Apple Silicon warning *"below the minimal requirements"*: expected. Webots
only lists discrete NVIDIA/AMD GPUs, so it turns shadows off. Physics and
sensors are unaffected.

When it opens you will see roughly:

```text
+--------------------------------+
|          3D WORLD              |
|         🤖      ████ wall      |
+--------------------------------+
 Scene Tree     Console     Controller
```

Do not panic. We only touch three things: the 3D view, the console, and
**Run**.

---

## 🌍 3. World, Robot, Controller

A **world** is the virtual environment — the file in `worlds/`.

```text
World
 ├── Floor
 ├── Walls
 ├── Obstacles
 ├── Robot
 └── LiDAR  (mounted on the robot)
```

A **robot** is the virtual machine: motors, wheels, camera, LiDAR, IMU, GPS.

A **controller** is Python that tells that machine what to do.

```text
Python
  ↓
controller
  ↓
robot
  ↓
motor
  ↓
wheel
  ↓
movement
```

The naming rule from Lesson 24 still applies: the folder name must match the
file name — `controllers/slam_scout/slam_scout.py` — or Webots fails silently.

---

## 🔴 4. What the LiDAR Does

LiDAR times a laser. Each beam is a distance in **metres**.

```text
        Wall
████████████████

   ← ← ← ←
      🤖
   → → → →
```

Typical one-scan report:

```text
Front = 2.4 m
Left  = 1.2 m
Right = 0.8 m
```

Webots exposes this as a `Lidar` node. The TurtleBot3's scanner is named
`LDS-01` and returns 360 beams (one per degree). You must call
`lidar.enable(timestep)` or every reading stays 0.

### Opposite of Lesson 26

| Sensor | Bigger number means |
|---|---|
| **LiDAR** (this lesson) | **Further** |
| **IR proximity** (e-puck, Lesson 26) | **Closer** |

Write `if value > 1` on the wrong sensor and the robot drives *into* the wall
with confidence.

---

## ⚠️ 5. We Are Not Coding SLAM Today

If I handed you Cartographer on day one you would press Run and learn
nothing. The pipeline is:

```text
Today
  Robot → LiDAR → distances → "wall / no wall"

Next
  LiDAR → odometry → SLAM → map → localization → navigation
```

One scan is a **snapshot**. SLAM is many snapshots, from many poses, glued
together with odometry and corrected by loop closure (Lesson 44). Keep that
distinction.

---

## 🔬 Practical — The Hallway

This repository is already a Webots project. Nothing to scaffold.

```bash
source .venv/bin/activate
python3 lidar_scan.py --test          # the maths, no simulator
python3 lidar_scan.py --demo          # a fake wall approaching 5 m → 0.7 m

open -a Webots worlds/slam_lab.wbt    # then press Run
```

[`worlds/slam_lab.wbt`](../worlds/slam_lab.wbt) is a long 8×3 m corridor.
A TurtleBot3 faces the far wall. One cardboard box sits on the right so left
and right readings are not the same.

[`controllers/slam_scout/slam_scout.py`](../controllers/slam_scout/slam_scout.py)
does exactly this:

```text
START
  ↓
motors ON, drive forward
  ↓
LiDAR: 5 m, 4 m, 3 m, 2 m, 1 m
  ↓
front < 1.0 m  →  motors OFF
  ↓
print one occupancy sketch from that pose
```

The decision is one line:

```python
if distance <= 1.0:
    stop
else:
    move_forward
```

That is **rule-based robotics**, not AI. It is also the Sense → Think → Act
loop from Lesson 10, now on a SLAM-class sensor.

Verified `--test` / `--demo` output (no Webots required):

```text
  wall 2.4 m ahead
  FRONT  2.40 m    LEFT  1.20 m    RIGHT  0.80 m
  decision: FORWARD  (front 2.40 m > 1.0 m)

  wall 0.7 m ahead
  FRONT  0.70 m    LEFT  1.20 m    RIGHT  0.80 m
  decision: STOP  (front 0.70 m <= 1.0 m)
```

Watch the **console** in Webots, not just the 3D view. The numbers are the
lesson. The occupancy sketch at the end is *one pose, one scan* — a drawing,
not a map.

The notebook [`lesson_45_slam_sim.ipynb`](../lesson_45_slam_sim.ipynb) walks
through the same functions cell by cell.

---

## 🔗 6. Same Architecture as a Real Robot

**Real**

```text
LiDAR → bytes → Python / C++ / ROS 2 → decision → motor driver → wheel
```

**Webots**

```text
Virtual LiDAR → simulation data → Python controller → decision → virtual motor
```

The boxes have the same names. That is why simulation-first is the industry
default, not a toy.

How this becomes SLAM:

```text
        WALL
██████████████████
      🤖  →  →  →

one scan          many scans + odometry
     ↓                    ↓
 snapshot              SLAM map
```

---

## 🛠️ Software stack (now vs later)

| Now | Purpose |
|---|---|
| VS Code / Cursor | Code |
| Python | Controller |
| GitHub | Portfolio |
| Webots R2025a | Simulation |
| OpenCV | Computer vision (already done) |

| Later | Purpose |
|---|---|
| ROS 2 | Middleware (`/scan` → SLAM Toolbox → `/map` → Nav2) |
| Gazebo / Isaac | Heavier simulation |
| Nav2 | Autonomous navigation |
| Jetson Orin Nano | Edge AI |
| Real LiDAR + depth camera | Physical sensors |

Not this week.

---

## 🎯 Exercises

1. Confirm Webots opens (`setup_check.py`).
2. Open `worlds/slam_lab.wbt`.
3. Press **Run**. Watch the robot drive. Read the console.
4. Find `controllers/slam_scout/slam_scout.py` — that is the brain.
5. Change `STOP_DISTANCE` in [`lidar_scan.py`](../lidar_scan.py) from `1.0` to
   `0.5`, reload the world, Run again. The robot should get closer.
6. Open the Scene Tree, select the TurtleBot, find `LDS-01`. That node is
   the sensor the Python asked for by name.
7. Optional: open [Tutorial 1](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?version=R2025a)
   if you want Cyberbotics' own "first simulation" as a second world.

Send a screenshot of Webots with the robot in the hallway if you want the
next click-by-click for Lesson 46 (sensor overlay, turning).

---

## 🎥 RoboticsFemme

**Title:** *I Built My First Robot Without Buying a Robot*

```text
MacBook → Webots → virtual robot → virtual LiDAR → stop at 1 m
```

Caption: *"Before buying expensive robotics hardware, I test the behaviour
inside simulation."*

Shot list: [Reel 8](../docs/reel-scripts.md).

---

## Mini quiz

| | Question | Answer |
|---|---|---|
| Q1 | What file is the virtual environment? | The `.wbt` **world** |
| Q2 | What file is the robot's brain? | The Python **controller** |
| Q3 | LiDAR: bigger number means? | **Further** (metres) |
| Q4 | Why enable the lidar? | Otherwise `getRangeImage()` stays empty / zero |
| Q5 | Is today's occupancy sketch SLAM? | **No** — one pose, one scan |

---

## 🚀 Next — Lesson 46: First Autonomous Robot in Webots

Same TurtleBot3, now it **turns** and keeps going:

```bash
open -a Webots worlds/slam_avoid.wbt
```

Press the green Play button. Do not run the controller from the terminal.

[Lesson 46](lesson-46-first-autonomous-robot.md)
