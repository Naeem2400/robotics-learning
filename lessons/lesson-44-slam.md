# Lesson 44 — SLAM: How a Robot Builds Its Own Map

**Module 18 — SLAM & Autonomous Navigation**

> The robot can see, track, and measure distance. Now it has to answer a
> harder pair of questions at the same time: **where am I, and what does this
> place look like?**

We already met the core idea in [Lesson 27](lesson-27-slam.md) with an ASCII
occupancy grid. This lesson is the industry version: LiDAR SLAM vs visual
SLAM, odometry drift, loop closure, ROS 2, and a **real HD video** you can
post on LinkedIn.

---

## 🎯 Lesson Goal

- What SLAM, localization, and mapping each mean — and why they are not the
  same thing
- Why indoor robots cannot rely on GPS
- LiDAR SLAM, visual SLAM, and visual-inertial SLAM
- Odometry, drift, and loop closure
- The names you will see in ROS 2: SLAM Toolbox, Cartographer, RTAB-Map,
  ORB-SLAM3
- A visual-odometry overlay on a free Full-HD clip

---

## 📖 1. What SLAM Is

**SLAM = Simultaneous Localization and Mapping.**

You leave a robot in a house it has never seen. Nobody gives it a floor plan.

```text
Robot
  ↓
looks at the room
  ↓
detects walls
  ↓
starts a map
  ↓
estimates its own position on that map
  ↓
moves
  ↓
updates the map
```

It is building the map **and** locating itself on that map at the same time.
That circular dependency is the whole difficulty.

---

## 🗺️ 2. Mapping

Mapping asks: **what does this place look like?**

```text
+----------------------+
|                      |
|      Room            |
|                      |
|          +------+    |
|          |      |    |
|          |      |    |
|          +------+    |
|                      |
+----------------------+
```

Walls, obstacles, and free space become cells (2D occupancy grid) or points
(3D point cloud). A map without a pose is a picture you cannot use.

---

## 📍 3. Localization

Localization asks: **where am I on the map?**

```text
+----------------------+
|                      |
|       🤖             |
|                      |
|          +------+    |
|          |      |    |
|          |      |    |
|          +------+    |
|                      |
+----------------------+
```

A pose without a map is a coordinate in an empty universe. The robot needs
both.

---

## 🔗 4. SLAM Combines Them

```text
             SLAM
              |
       +------+------+
       |             |
   Mapping       Localization
       |             |
  the world      where am I?
       |             |
       +------+------+
              |
        Navigation
```

A fourth word sits on top: **navigation** — "where do I go next?" That is
Lesson 45 / Nav2. Do not mix the four up:

| Term | Question |
|---|---|
| Mapping | What does the environment look like? |
| Localization | Where am I? |
| Navigation | Where do I need to go? |
| **SLAM** | Build the map **and** estimate the pose, together |

---

## 📡 5. Why Not Just GPS?

Outdoors, GPS is useful to a few metres. Indoors:

```text
🏠  walls block the satellites
```

A robot vacuum, a warehouse AMR, a hospital trolley — none of them get a
trustworthy GPS fix. They use **LiDAR, cameras, IMUs, and wheel encoders**
instead.

---

## 🔴 6. LiDAR SLAM

LiDAR fires laser beams and times the reflection.

```text
        Wall
████████████████

  ↗ ↑ ↖
   \|/
    🤖
```

Each beam is a range. A full scan is a slice of the room. Stack scans as the
robot moves and you get a geometric map — the occupancy grid from Lesson 27.

Hallway:

```text
Wall                    Wall
██████                 ██████
      \               /
       \     🤖      /
        \           /
████████████████████████
```

LiDAR sees the left wall, the right wall, whatever is in front. The map grows
scan by scan.

---

## 📷 7. Visual SLAM

Same job, a camera instead of a laser.

```text
Camera
  ↓
image
  ↓
features (corners, edges)
  ↓
motion estimate
  ↓
map + pose
```

The robot does not need to "understand" the room. It needs **features it can
recognise again** — book spines, door frames, the corner of a table.

---

## ⚖️ 8. LiDAR vs Visual

| LiDAR SLAM | Visual SLAM |
|---|---|
| Laser ranges | Camera images |
| Accurate geometry | Rich appearance |
| Expensive sensor | A camera is cheap |
| Works in the dark | Needs light (or an IR camera) |
| Strong at mapping walls | Strong at recognising places |

Both are used in production. Robot vacuums are usually LiDAR (or a mix).
Tesla's stack is famously camera-first. Warehouse robots often run LiDAR +
wheel odometry, with cameras for extras.

---

## 🧭 9. Visual-Inertial SLAM

```text
Camera + IMU  →  Visual-Inertial SLAM
```

The IMU measures acceleration and angular velocity. Between camera frames it
tells you how the robot rotated and lurched. The camera corrects the IMU's
drift; the IMU covers the blurry frames. Phones (ARKit, ARCore) and drones
do this. ORB-SLAM3 can run in this mode.

---

## 🛞 10. Odometry — and Why It Drifts

Odometry: **estimate motion from the robot's own movement sensors.**

```text
wheel encoder  →  rotation  →  distance travelled  →  pose
```

"I have moved about one metre since the last tick."

The problem is **drift**. Every small slip, rounding error, and unmodelled
bump is added to the next one. After a long corridor the believed pose and
the true pose have quietly walked apart:

```text
actual     🤖
estimated     🤖     ← same robot, two answers
```

Lesson 27's second pass is exactly this: correct laser hits written into the
wrong cells, walls doubling up, accuracy collapsing.

---

## 🔄 11. Loop Closure

SLAM's answer to drift: **recognise a place you have already been.**

```text
START
  ↓
A → B → C
↑       ↓
F ← E ← D
  ↓
back at START  →  "I know this doorway"
  ↓
correct the whole trajectory
  ↓
the map snaps consistent
```

That recognition-and-correction step is **loop closure**. Without it, a
twenty-minute mapping run becomes the smeared map from Lesson 27. With it,
the robot can map a whole floor.

---

## 🏗️ 12. The Pipeline

```text
Sensors
  ↓
Odometry
  ↓
Scan / feature matching
  ↓
Pose estimation
  ↓
Map update
  ↓
Loop closure
  ↓
Optimised map
```

Remember this architecture. Every SLAM package is a different implementation
of the same diagram.

---

## 🧰 13. Names You Will See

Start recognising these. You do not install them today.

| System | What it is |
|---|---|
| **ORB-SLAM3** | Research-grade visual / visual-inertial SLAM |
| **RTAB-Map** | RGB-D, stereo, and LiDAR; common on real robots |
| **Cartographer** | Google's LiDAR SLAM (2D and 3D) |
| **SLAM Toolbox** | The default 2D SLAM package in ROS 2 |

---

## 🧩 14. ROS 2 Sketch

Later the topics look like this:

```text
LiDAR
  ↓
/scan
  ↓
SLAM Toolbox
  ↓
/map
  ↓
localization
  ↓
Nav2
  ↓
the robot actually moves
```

That is the first time ROS 2 topics stop being a metaphor and start being
the wiring of a real system. We stay on the MacBook until the wiring is
clear.

---

## 🌍 15. Two Real Systems

**Robot vacuum**

```text
start → scan the room → walls → move → update map → next room → finished map
```

Then it remembers kitchen / living room / hall and plans an efficient clean.

**Warehouse robot**

```text
LiDAR → SLAM → warehouse map → localization → Nav2 → Shelf A → packing station
```

Same pipeline, bigger building, tighter tolerances.

The future Jetson stack you have sketched (Orin Nano + LiDAR + depth camera
+ ROS 2) is this diagram on real hardware. We practise it in simulation
first. No purchase required.

---

## 🔬 Practical — Visual SLAM on a Free HD Clip

You have no LiDAR on the desk. You have a camera stack from Lessons 30–43.
That is enough to **watch visual SLAM happen on a real moving camera**.

```bash
source .venv/bin/activate

python visual_slam.py --test          # the maths, no video
python visual_slam.py --linkedin      # downloads a free Full-HD clip, overlays SLAM
python visual_slam.py --linkedin --reel --gif
```

[`visual_slam.py`](../visual_slam.py) does four things:

1. Downloads Mixkit clip **#21589** (library corridor, 1920×1080, Mixkit
   Stock Video Free License — commercial use allowed, no faces). Saved to
   `video_out/` so it is not committed.
2. Tracks hundreds of corners with optical flow — the features a visual-SLAM
   front-end actually uses.
3. Integrates that motion into a pose (**odometry**) and draws a bird's-eye
   **map**.
4. Renders a 1920×1080 dashboard: camera + map + the four terms on screen,
   with a 2-second hook and a 3-second closer. Output:
   `video_out/slam_linkedin_landscape.mp4`.

Pass `--video your.mp4` to run the same overlay on any clip. A phone pan
around your own room is the most honest version.

The notebook [`lesson_44_slam.ipynb`](../lesson_44_slam.ipynb) walks through
the same ideas cell by cell.

> This demo is **visual odometry**, the front-end of visual SLAM. A production
> system (ORB-SLAM3, RTAB-Map) also bundle-adjusts the map and closes loops
> across a full graph. The LinkedIn video is the intuition; those packages
> are the engineering.

Verified `--test` output:

```text
  Lesson 44 tests passed.
  odometry integrates, loop-closure needs BOTH distance and recognition,
  and optical flow tracks a moving texture.
```

---

## 💻 Software-First Path

```text
MacBook
  ↓
this demo  /  Webots  /  Gazebo
  ↓
virtual LiDAR or a camera
  ↓
SLAM
  ↓
a map
```

Hardware later. Concepts now.

---

## 🎯 Mini Quiz

| | Question | Answer |
|---|---|---|
| Q1 | SLAM in full? | Simultaneous Localization and Mapping |
| Q2 | What does LiDAR measure? | Distance, by timing a laser |
| Q3 | Estimating the robot's pose? | Localization |
| Q4 | Recognising a previous place and correcting the map? | Loop closure |
| Q5 | Estimating motion from wheel / camera motion? | Odometry |

---

## 🎥 RoboticsFemme — Reel / LinkedIn

**Hook (on screen, works muted):**

> How does a robot build a map when nobody gives it one?

Then the dashboard: features lighting up, the map growing, the pose ticking.

**Closer:**

> The robot is simultaneously learning the world and finding itself inside it.

Shot list and caption: [Reel 7 in `docs/reel-scripts.md`](../docs/reel-scripts.md).

---

## 🏆 Portfolio

**Autonomous robot mapping with SLAM** — a LinkedIn-ready overlay on a
licensed HD clip, plus the Lesson 27 occupancy-grid demo that proves why
mapping without localization is useless.

Next implementation (Lesson 45): the same ideas on a Webots robot with a
virtual LiDAR, then ROS 2.

---

## 📊 Progress

Lesson **44 / ~250**.

| Phase | Status |
|---|---|
| Robotics foundation | done |
| Basic computer vision | done |
| AI vision | almost done |
| **SLAM & autonomous navigation** | **starting now** |
| ROS 2 (practical stack) | next |
| Jetson / LiDAR hardware | later |
| Physical AI / humanoids | advanced |

---

## 🚀 Next — Lesson 45: First SLAM Robot in Webots

Open the hallway and press Run:

```bash
open -a Webots worlds/slam_lab.wbt
```

A TurtleBot3 drives toward a wall, prints LiDAR metres, and stops at 1 m.
That is the measurement SLAM is made of — not SLAM itself yet.

[Lesson 45](lesson-45-slam-simulation.md)
