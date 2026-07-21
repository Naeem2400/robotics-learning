# Lesson 27 — SLAM (Simultaneous Localization and Mapping)

**Module 14 — Autonomous Robotics**

> Understand SLAM and you understand how Tesla, robot vacuums, warehouse
> robots, and humanoids navigate **without GPS**.

---

## 🎯 Lesson Goal

- What SLAM is
- What localization is
- What mapping is
- How a robot moves through a room with no GPS
- The role of LiDAR
- How SLAM is used in ROS 2

---

## 📖 1. A Story First

Imagine walking into a huge shopping mall for the first time with no map, no
GPS, and no guide.

You look around. You start walking. You remember: *"the food court was there,"*
*"the lift was here,"* *"there was a red shop at that corner."*

Slowly, a map of the mall forms in your head — **while you are moving through
it**. You are working out where you are and what the place looks like at the
same time.

A robot does exactly this.

---

## 🧩 2. The Two Problems

SLAM = **S**imultaneous **L**ocalization **A**nd **M**apping.

| Problem | Question | Name |
|---|---|---|
| 1 | *Where am I?* | **Localization** |
| 2 | *What does this place look like?* | **Mapping** |

### Why neither works alone

- **Mapping only** → the robot builds a map but does not know where it is on it
- **Localization only** → the robot knows its position but has no map to
  navigate

**Localization + Mapping = SLAM**, and the hard part is that each one *needs
the other*. To place a wall on the map you must know where you were standing.
To know where you are standing you must recognise the walls. This circularity
is what makes SLAM a genuinely hard problem, not just two easy ones.

---

## 🔬 3. Practical — See Why They Cannot Be Separated

```bash
python3 slam_demo.py
```

[`slam_demo.py`](../slam_demo.py) drives a robot around the same room twice,
building a map from simulated laser scans.

### Pass 1 — the robot knows exactly where it is

```text
    ########################################
    #......................................#
    #....########..........................#
    #....#      #..............######......#
    #....########..............#....#......#
    ########################################

    481 cells discovered, 100.0% correct
```

A perfect map.

### Pass 2 — the same robot, but its position slowly drifts

```text
     ####        #########
    ###.####    ############################
    ##.####.     #..........................
    ##.##...     #.#...........##.   .#.....
    ##.###########.............###...##.....
    ########################################

    463 cells discovered, 69.1% correct
    final position error: 3.3 cells
```

The walls **smear and double up**. The room is unrecognisable.

### The point

Nothing changed about the sensor. Every laser measurement in pass 2 was
**exactly as accurate** as in pass 1. The only difference is that the robot's
belief about its own position drifted by about 3 cells.

> **The lidar was never wrong. The position was.**

Correct measurements written into the wrong cells produce a useless map. This
is why you cannot "just do mapping" — and why real robots must estimate
position and map **together**, correcting each against the other.

---

## 📡 4. Sensors

| Sensor | Purpose |
|---|---|
| LiDAR | Distance scanning |
| Camera | Vision |
| Depth camera | 3D understanding |
| IMU | Rotation and acceleration |
| Wheel encoders | How far the wheels turned |
| GPS | Outdoor position only |

### What LiDAR does

Think of a torch that emits laser instead of light, sweeping in every
direction and measuring the distance to whatever it hits:

```text
        *
     *     *
   *   🤖   *
     *     *
        *
```

Each `*` is one measurement. Our TurtleBot in Lesson 10 used exactly this — 360
beams, one per degree.

### Why not GPS indoors?

GPS signals are weak or absent inside buildings, and even outdoors it is
accurate only to a few metres — useless for a robot that must avoid a table
leg. So indoor robots rely on LiDAR, cameras, IMUs, and encoders.

### Where the drift in our demo comes from

Wheel encoders count rotations to estimate movement — this is **odometry**. But
wheels slip, floors vary, and tiny rounding errors accumulate. Odometry error
**only ever grows**; nothing corrects it. That is precisely what pass 2
simulates, and why real SLAM continually re-anchors the position against
recognised landmarks.

---

## 🏗️ 5. SLAM Architecture

```text
LiDAR ─┐
Camera ─┤
IMU ────┼──> Sensor fusion ──> SLAM ──┬──> Map
Encoders┘                             └──> Robot position
                                              │
                                              ▼
                                        Path planner
                                              │
                                              ▼
                                       Motor controller
```

This is the brain of a modern autonomous robot.

---

## 🤖 6. SLAM in ROS 2

Popular packages:

| Package | Notes |
|---|---|
| `slam_toolbox` | The common default for 2D lidar SLAM |
| `Cartographer` | From Google, 2D and 3D |
| `RTAB-Map` | Vision and RGB-D based |

You will use these later. For now the concept matters more than the package.

### Real companies

| Company | Approach |
|---|---|
| **Tesla** | Vision-based localization |
| **Boston Dynamics** | LiDAR + cameras + IMU |
| **Amazon Robotics** | Warehouse mapping |
| **NASA Mars rovers** | SLAM-like navigation on unknown terrain |
| **Figure AI** | Humanoids mapping their environment |

---

## ⚠️ 7. Common Mistakes

- **Thinking only LiDAR can do SLAM.** Visual SLAM uses cameras alone; Tesla
  does not use lidar at all.
- **Confusing mapping with localization.** Run the demo — the difference is
  the whole lesson.
- **Assuming every robot needs GPS.** Most indoor robots never use it.
- **Trusting odometry alone.** It always drifts. Pass 2 shows what that costs.
- **Expecting a perfect map.** Real SLAM maps are probabilistic and noisy;
  "good enough to navigate" is the goal.

---

## 🎯 8. Interview Questions

**Q: What is the main purpose of SLAM?**

> SLAM lets a robot build a map of an unknown environment while estimating its
> own position within that map at the same time.

<details>
<summary>Q: Why is it "simultaneous"? Why not map first, then localize?</summary>

Because each depends on the other. Building a map requires knowing where you
were when you took each measurement, and knowing where you are requires
recognising features in the map. Neither can be completed first, so the two
are estimated together and continuously corrected against each other. This is
the whole difficulty of SLAM — and exactly what `slam_demo.py` demonstrates by
letting the position drift.
</details>

<details>
<summary>Q: What is loop closure?</summary>

When a robot returns to a place it has already mapped, it can recognise the
location and correct all the drift accumulated since it was last there. Loop
closure is what keeps long-running SLAM from degenerating into the smeared map
of pass 2 — a large correction applied backwards through the whole trajectory.
</details>

---

## 🧠 Mini Challenge

A robot enters a new office with no GPS. How does it navigate?

> It observes the environment with its sensors (LiDAR, camera, IMU, encoders),
> builds a map using SLAM, and estimates its position within that map.

**Then try this:** open `slam_demo.py` and change `DRIFT_PER_STEP` from `0.045`
to `0.005`. Accuracy climbs back toward the clean run. Set it to `0.2` and the
map becomes noise. **How much drift a robot can tolerate is a real engineering
number**, not a detail.

---

## 💡 9. 2026 Industry Reality

Advanced robots do far more than SLAM alone:

```text
Sensors → Sensor fusion → SLAM → Localization → Path planning
   → Obstacle avoidance → AI vision → LLM reasoning → Robot actions
```

---

## 🚀 Next — Lesson 28: Path Planning

The robot now has a map. **How does it choose the best route?**

- A* algorithm
- Dijkstra
- RRT
- Nav2 (the ROS 2 navigation stack)
- How warehouse robots and delivery robots plan routes

Plus, from here on, the **industry architecture** behind each topic: which
algorithm is used when, its computational cost, what real companies choose,
and when AI replaces classical robotics versus combining with it.
