# Lesson 46 — Webots + Python: First Autonomous Robot

**Module 18 — SLAM & Autonomous Navigation**

> Lesson 45 stopped at the wall. Today the robot **decides**: move, detect,
> stop, turn toward the open side, keep going. That is your first autonomous
> mobile robot. You already have Webots — this lesson is how to **run the
> code inside it**.

```text
Robot moves
      ↓
LiDAR sees a wall
      ↓
STOP
      ↓
TURN (toward the clearer side)
      ↓
FORWARD again
```

---

## 🎯 Lesson Goal

- What “autonomous” means here (rule-based, not AI)
- Differential-drive: how two wheels make forward vs turn
- Sense → Think → Act as a live loop
- **How to open this project in Webots and press Run**
- What to look at if nothing moves

**Do not install ROS 2.** Do not buy a LiDAR.

---

## 1. Autonomous, in one sentence

An autonomous robot uses sensor data to **choose its own next action**. You
are not clicking “go left”. The Python controller is.

```text
Sensor → information → decision → motor → movement
```

Wall at 0.7 m → STOP → TURN. That loop, forever, is autonomy at Level 2–3
of this course. Deep learning comes later.

---

## 2. How to run it (you already have Webots)

Do this from the **Robotics** folder — the same folder that contains
`worlds/` and `controllers/`. Webots only finds controllers if those two
folders sit next to each other.

### Step 1 — Open the world

In Terminal:

```bash
cd ~/Documents/Robotics
open -a Webots worlds/slam_avoid.wbt
```

Or in Webots: **File → Open World…** and choose
`worlds/slam_avoid.wbt`.

First open may download the TurtleBot3 PROTO from GitHub. Wait until the 3D
hallway appears.

### Step 2 — Show the console

You need two windows of attention: the robot **and** the numbers.

**Tools → Console** (if the bottom panel is missing).

### Step 3 — Press Run

Toolbar: the green **▶ Play** button.

You should see:

1. The TurtleBot drive down the hallway.
2. Console lines like:

```text
[  0.03s] FORWARD   front 3.41 m
[  4.80s] TURNING   front 0.97 m toward LEFT  (L 1.85  R 0.72)
[  6.40s] FORWARD   front 1.42 m
```

3. The robot spin toward the more open side, then drive again.

**Pause** is the yellow `||`. **Reload World** (circular arrow) restarts from
the start pose after you edit Python.

### Step 4 — Confirm the controller is attached

Scene Tree (left) → click `TurtleBot3Burger` → find the `controller` field.

It must say **`slam_avoider`**.

If it says `slam_scout` you still have Lesson 45’s world
(`slam_lab.wbt`) open. Close it and open `slam_avoid.wbt`.

To attach it by hand: click the field → **Select…** → `slam_avoider`.

### Do **not** do this

```bash
python3 controllers/slam_avoider/slam_avoider.py
```

That fails with `No module named 'controller'`. The `controller` package is
injected by Webots when **it** starts the file, not when the terminal does.

---

## 3. What the brain is doing

[`controllers/slam_avoider/slam_avoider.py`](../controllers/slam_avoider/slam_avoider.py)
is the robot. [`lidar_scan.py`](../lidar_scan.py) holds the decision maths so
we can test it without the simulator.

```text
              ROBOT
                |
       +--------+--------+
       |                 |
    LiDAR              Motors
       |                 |
       ↓                 ↑
   front/left/right   wheel speeds
       |
       ↓
 Python controller
```

Two states (a tiny finite state machine):

| State | Motors | Until |
|---|---|---|
| **FORWARD** | both wheels same speed | front ≤ 1.0 m |
| **TURNING** | wheels opposite (spin in place) | front > 1.3 m |

The 1.0 vs 1.3 gap is **hysteresis** — without it the robot flickers
FORWARD/TURNING every frame at the boundary. Lesson 26 used the same idea
on IR sensors.

Turn direction: **whichever side is more open**.

```python
if front <= 1.0:
    if left >= right:
        turn_left()
    else:
        turn_right()
else:
    move_forward()
```

Example: front 0.5 m, left 2.0 m, right 0.8 m → **turn left**.

Try it without Webots:

```bash
python3 lidar_scan.py --test
```

---

## 4. Two wheels

```text
       FRONT
        🤖
   O          O
 Left       Right
```

| Left wheel | Right wheel | Result |
|---|---|---|
| → same speed | → same speed | **Forward** |
| ← | → | **Spin left** on the spot |
| → | ← | **Spin right** on the spot |
| slow | fast | Curve right |

That is **differential drive**. Almost every indoor mobile robot uses it
(TurtleBot, robot vacuum, many AMRs).

---

## 5. Sense → Think → Act

This is the sentence to keep:

> **Autonomous robotics = Sense → Think → Act**

```text
SENSE   LiDAR front = 0.7 m
THINK   0.7 ≤ 1.0  →  blocked; left is clearer
ACT     spin left
SENSE   (repeat forever)
```

`while robot.step(timestep) != -1:` is that forever. `Robot()` connects
Python to the simulated machine. `step()` advances physics by one tick.

Same boxes as a future Jetson robot:

```text
LiDAR → Jetson / ROS 2 → decision → motor driver → wheels
```

Webots replaces the physical LiDAR and the motor driver. The Python in the
middle is the skill you are practising.

---

## 6. This is not AI

Rule-based autonomous robotics. `if/else`. Later we replace the `if` with
perception, planning, learning — but a planner that cannot stop for a wall
is useless. You are at **Level 2 → Level 3**:

```text
1 Manual control
2 Rule-based avoidance     ← Lesson 45 stop, Lesson 46 turn
3 Sensor-based navigation
4 SLAM
5 Autonomous navigation (Nav2)
6 AI perception
7 AI planning
8 Embodied AI
```

---

## 7. Three tests in this world

[`worlds/slam_avoid.wbt`](../worlds/slam_avoid.wbt) is a hallway with two
boxes, one on each side, so the robot has a real left/right choice.

| Test | What you do | What should happen |
|---|---|---|
| **1 — open path** | Press Run | Drives forward, console says `FORWARD` |
| **2 — wall / box ahead** | Wait | `TURNING toward LEFT` or `RIGHT`, then `FORWARD` again |
| **3 — both sides tight** | In Scene Tree, drag the second box in front of the robot as well | It still picks the **slightly** more open side. Watch. It may look “stuck” while spinning — read the console |

To retry: **Reload World**, then **Run**.

To change the stop distance: edit `STOP_DISTANCE` in `lidar_scan.py`, save,
**Reload World**, Run. The controller imports that number.

---

## 8. If the robot does not move

This checklist is the same one you will use on a real robot.

1. Is the simulation **running** (green Play), not paused?
2. Is the world **`slam_avoid.wbt`** (title bar)?
3. Scene Tree → robot → `controller` = **`slam_avoider`**?
4. Console: any red Python traceback?
5. Folder names: `controllers/slam_avoider/slam_avoider.py` — names must
   match exactly (Lesson 24).
6. Did you `lidar.enable(timestep)`? (already in this controller)
7. Device name **`LDS-01`** — that is the TurtleBot3 lidar. `ps0` is the
   e-puck IR from Lesson 26; wrong name → crash or zeros.
8. Motors in velocity mode: `setPosition(float("inf"))` then
   `setVelocity(...)`. Missing the inf line = wheels lock.

Apple Silicon “below minimal requirements”: ignore. It only drops shadows.

---

## 9. How this differs from earlier lessons

| Lesson | Robot | Sensor | Behaviour |
|---|---|---|---|
| 25 | e-puck | none | Blind timed drive |
| 26 | e-puck | IR (`ps0`…), **bigger = closer** | Avoid |
| 45 | TurtleBot3 | LiDAR metres, **bigger = further** | Drive, **stop** |
| **46** | TurtleBot3 | LiDAR metres | Drive, **turn, continue** |

Same Sense → Think → Act. Different sensor. Different policy.

---

## Mini quiz

| | Question | Answer |
|---|---|---|
| Q1 | Why not `python3 slam_avoider.py`? | `controller` exists only inside Webots |
| Q2 | Both wheels same speed? | Forward |
| Q3 | Why 1.0 m stop and 1.3 m clear? | Hysteresis — stop flickering |
| Q4 | Front 0.5, left 2.0, right 0.8? | Turn **left** |
| Q5 | Is this machine learning? | **No** — rule-based autonomy |

---

## 🎥 RoboticsFemme

**“My Robot Makes Its Own Decisions”**

Screen-record Webots (3D + console). Caption: *This is not remote control.
The robot senses the hallway and chooses left or right.*

Shot list: [Reel 9](../docs/reel-scripts.md).

---

## 🚀 Next — Lesson 47: Robot Sensors in Detail

Which sensor for which job: ultrasonic, IR, LiDAR, camera, depth camera,
IMU, wheel encoder, GPS, force/torque — then **sensor fusion**
(LiDAR + camera + IMU + encoders). That is the stack for the future
Jetson + LiDAR + depth camera + ROS 2 robot.
