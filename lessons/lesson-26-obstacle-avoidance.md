# Lesson 26 — Obstacle Avoidance Robot

**Project 2 — The First Intelligent Robot**

> In the last lesson the robot was **blind**. It only knew how to move.
> Today it starts to **think**. This is where robotics gets interesting.

---

## 🎯 Lesson Goal

- What a distance sensor is
- How a robot detects an obstacle
- How it makes a decision
- The basic autonomous robot algorithm
- An introduction to the Finite State Machine (FSM)

---

## 📖 1. The Idea

Imagine walking with your eyes closed toward a wall. What do you do?

| Human | Robot |
|---|---|
| 👀 Eyes | 📡 Sensor |
| 🧠 Brain | 🤖 Controller |
| 🚶 Stop | ⚙️ Motors |

Same concept.

## What Is a Distance Sensor?

A sensor that measures how far away an object is. It acts as the robot's eyes,
continuously asking: *"is there something in front of me?"*

| Sensor | Range | Typical use |
|---|---|---|
| Ultrasonic | 2 cm – 4 m | Arduino robots |
| Infrared (IR) | Short range | Line and obstacle robots |
| LiDAR | 0.1 – 100+ m | Self-driving, mapping |
| Depth camera | RGB + distance | AI robots |

We use the e-puck's built-in **IR proximity sensors**. Different hardware,
identical concept.

---

## 🏗️ 2. Architecture

```text
Distance sensor → read value → compare to threshold → decision
     → motor command → robot moves
```

This is the Sense → Think → Act loop from Lesson 10, now with real sensors on
a real robot.

---

## ⚠️ 3. Understanding Sensor Values

Suppose a sensor outputs: `15, 20, 30, 55, 90, 150`.

**Does 150 mean the obstacle is close?**

⚠️ **It depends on the sensor**, and this is the single most important idea in
the lesson.

| Sensor type | Bigger number means |
|---|---|
| **IR proximity** (e-puck) | **Closer** — more light bounced back |
| **LiDAR** | **Further** — it reports distance in metres |

These are **opposite**. Write `if value > threshold` on the wrong sensor and
your robot drives *into* walls with confidence.

> We hit this exact difference earlier in the course: the TurtleBot's lidar in
> Lesson 10 reported metres (small = close), while the e-puck's IR sensors
> report intensity (large = close). Reading the documentation is not optional —
> it is the job.

### The e-puck's sensor layout

```text
        ps7   ps0
          \   /
    ps6 --(ROBOT)-- ps1
          /     \
        ps5     ps2
```

`ps0` and `ps7` face forward. Reading roughly 0 in open space, climbing into
the hundreds as a wall approaches.

---

## 🧠 4. The Algorithm

```text
Start → move forward → read sensor → obstacle?
   ├─ No  → keep moving forward
   └─ Yes → turn → resume
   (repeat forever)
```

```python
while True:
    distance = read_sensor()
    if distance > threshold:
        turn()
    else:
        move_forward()
```

## Finite State Machine

Professional robots do not scatter `if-else` everywhere. They use a **state
machine** — the robot is always in exactly one state:

```text
   MOVING ──obstacle──> TURNING
      ^                    │
      └────path clear──────┘
```

Each state has its own behaviour and its own rules for leaving.

---

## 🔬 5. Practical — Run It

```bash
open -a Webots worlds/movebot_avoid.wbt      # then press Run
```

MoveBot now drives around an arena containing four boxes, steering away from
each one and from the walls. Console output:

```text
[  0.06s] MOVING   (sensor    0.0) path clear
[  3.14s] TURNING  (sensor  102.4) turning left
[  4.35s] MOVING   (sensor   48.1) path clear
```

The code is
[`controllers/movebot_avoider/movebot_avoider.py`](../controllers/movebot_avoider/movebot_avoider.py).

### Two design details worth understanding

**1. Two thresholds, not one.**

```python
OBSTACLE_THRESHOLD = 80.0   # start turning above this
CLEAR_THRESHOLD    = 60.0   # only resume driving below this
```

If both were `80`, the robot would flicker between MOVING and TURNING at the
boundary, twitching in place. The gap between them is called **hysteresis**,
and every real controller uses it.

**2. It turns away from the blocked side.**

```python
turn_direction = -1 if front_right > front_left else 1
```

Always turning the same way gets a robot stuck in corners — which we saw
happen in Lesson 10.

---

## 🌍 6. Real World

| Robot | Behaviour |
|---|---|
| **Warehouse robot** | Shelf detected → stop → recalculate path → continue |
| **Tesla** | Camera → person detected → brake → wait → continue |

Same concept, more advanced sensors.

### Sensor fusion

Real robots never rely on one sensor:

```text
Camera + LiDAR + IMU + GPS → robot brain → decision
```

---

## ⚠️ 7. Common Mistakes

- **Forgetting `sensor.enable(TIME_STEP)`** — `getValue()` then returns 0
  forever and the robot cheerfully drives into walls. No error appears.
- **Choosing a threshold at random** — print the values first and watch how
  they change as you approach a wall.
- **Comparing without knowing the sensor's direction** — see section 3.
- **Using one threshold instead of two** — causes twitching.
- **Printing every loop iteration** — 15 lines per second buries anything
  useful. Print on state *changes*.

---

## 🎯 8. Interview Question

**What is the basic obstacle-avoidance algorithm?**

> The robot reads its sensors continuously. If an obstacle is nearer than the
> threshold it changes direction; otherwise it keeps moving forward.

<details>
<summary>Why is a state machine better than a plain if-else?</summary>

An `if-else` decides fresh on every loop with no memory, so a robot at the
edge of the threshold flips between behaviours many times per second. A state
machine **remembers** what it is doing and defines explicit rules for leaving
that state, which makes behaviour stable and predictable. It also scales: adding
a `BACK` or `CHARGING` state is a small change, whereas nested if-else grows
unmanageable.
</details>

---

## 🧠 Mini Challenge

| Threshold | Sensor | Robot does |
|---|---|---|
| 80 | 40 | **Move forward** — 40 < 80, nothing close |
| 80 | 150 | **Turn** — 150 > 80, obstacle detected |

Then try it for real: change `OBSTACLE_THRESHOLD` to `30` and re-run. The
robot becomes nervous, turning at shadows. Set it to `200` and it clips the
boxes. **Tuning thresholds is real engineering work**, not guesswork.

---

## 🌍 9. What Professionals Do Instead

Today's robot only turns left or right. A production robot does:

```text
Obstacle → update map → SLAM → path planning → best route → move
```

That is the difference between a beginner robot and an Amazon warehouse robot:
ours **reacts**, theirs **plans**.

---

## 🚀 Next — Lesson 27: SLAM

**Simultaneous Localization and Mapping** — used by robot vacuums, Tesla,
delivery robots, warehouse robots, Boston Dynamics, and NASA rovers.

- How does a robot know where it is without GPS?
- How does it build a map?
- How does it navigate an unknown room?

```text
Reactive robot ✅ → SLAM → Navigation → Path planning
   → Sensor fusion → AI vision → LLM reasoning → Humanoid intelligence
```

This is where robotics engineering and AI engineering genuinely merge.
