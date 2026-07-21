# Lesson 28 — Path Planning

**Module 15 — Navigation**

> SLAM gave the robot a **map**. Now: **how does it find the best route to its
> destination?**

---

## 🎯 Lesson Goal

- What path planning is
- The difference between a route and a path
- The A* algorithm
- Dijkstra's algorithm
- RRT (Rapidly-exploring Random Tree)
- The role of ROS 2 Nav2

---

## 📖 1. The Idea

You need to get to the airport. Google Maps offers three routes — 20, 30, and
45 minutes. You pick the 20-minute one.

A robot does exactly the same thing.

### Definition

Path planning is the algorithmic process of calculating a **safe and efficient
path from a start point to a goal point**.

The robot must decide: where to go, which way to get there, and which
obstacles to avoid.

### Route vs Path

| | Meaning | Example |
|---|---|---|
| **Route** | General direction | Multan → Lahore |
| **Path** | The exact sequence of moves | straight → left → straight → right |

A robot needs a **path**.

### Where it fits

```text
Robot start → Localization → SLAM → Map ready
   → Path planning → Motor commands → Robot moves
```

---

## 🗺️ 2. The Grid Map

The world gets divided into cells:

```text
S . . . .
X X . X .
. . . X .
. X . . G
```

`S` start · `G` goal · `X` obstacle · `.` free space

The job: get from S to G without touching an X.

---

## 🔬 3. Practical — Dijkstra vs A*, Measured

Everyone is told *"A* is faster because it uses a heuristic."* Let us prove it.

```bash
python3 path_planning_demo.py
```

[`path_planning_demo.py`](../path_planning_demo.py) runs both algorithms on the
same map and counts how many cells each one examined.

### Dijkstra

```text
    S***oooooooo#oooo.....
    ooo*oooooooo#oooo.....
    ooo*####ooo.#..####...
```

### A*

```text
    S***oooooo#..........
    ooo*oooooo#..........
    ooo*####oo#..####....
```

### The result

| | Path length | Cells examined |
|---|---|---|
| Dijkstra | 30 steps | 161 |
| **A\*** | **30 steps** | **114** |

**Both found a path of the same length** — both are optimal. But A* did
**29% less work**.

Look at the `o` marks in the two maps. Dijkstra's spread out in a circle around
the start, searching in *every* direction equally. A*'s stretch **toward the
goal**. Same answer, less effort.

---

## 🧮 4. How They Differ (they are the same algorithm)

This surprises people: A* and Dijkstra are the **same code**. Only one line
differs — how they choose which cell to examine next:

```python
priority = new_cost                             # Dijkstra
priority = new_cost + heuristic(cell, goal)     # A*
```

| | Chooses the cell with… |
|---|---|
| **Dijkstra** | the lowest cost **so far** |
| **A\*** | lowest cost so far **+ estimated cost remaining** |

That estimate is the **heuristic** — the robot's guess at *"how far is the goal
from here?"* It stops the search wandering away from the goal.

> **⚠️ The heuristic must never overestimate** the true remaining distance. If
> it does, A* can return a path that is not the shortest. Our demo uses
> Manhattan distance, which with 4-way movement is exactly correct — never too
> high. A heuristic with this property is called *admissible*, and it is the
> difference between A* being reliable and A* being merely fast.

---

## 🌲 5. The Three Algorithms

### Dijkstra

Evaluates every possible route.

✅ Guaranteed shortest path ❌ Slow on large maps

### A*

Uses a heuristic to search toward the goal.

✅ Fast and still optimal ❌ Needs a sensible heuristic

Used in indoor robots, warehouse robots, games, drones, delivery robots.

### RRT (Rapidly-exploring Random Tree)

Grows random branches outward until one reaches the goal:

```text
Start
  ├──
  ├────────
  └─────── Goal
```

Useful in **complex, high-dimensional** spaces — which is why it dominates
**robot arms**. A grid works for a robot on a floor (2 dimensions), but an arm
with 6 joints has a 6-dimensional space that no grid can cover. RRT samples it
instead.

| Algorithm | Speed | Accuracy | Used for |
|---|---|---|---|
| Dijkstra | Slow | Optimal | Small maps |
| A* | Fast | Optimal | Mobile robots |
| RRT | Medium | Good enough | Robot arms, complex spaces |

---

## 🤖 6. ROS 2 Nav2

Real robots do not hand-write A*. They use the ROS 2 navigation stack,
**Nav2**:

```text
Goal → Global planner (A*) → Local planner (obstacle check)
   → Motor controller → Robot
```

| Planner | Job |
|---|---|
| **Global** | Looks at the whole map and plans the overall route |
| **Local** | Reacts *now* — someone steps in front, replan immediately |

### Why two planners?

Because replanning the entire route every time a person walks past would be far
too slow. The global plan is computed rarely; the local planner runs many times
a second on just the robot's surroundings.

```text
Warehouse robot: shelf → route ready → person appears → new local path → continue
Tesla:           road → pedestrian → brake → new path → continue
```

### Static vs dynamic obstacles

A chair is **static** — it belongs on the map. A human is **dynamic** — they
move, so they must be handled live by the local planner. Robots must deal with
both, which is exactly why the stack is split in two.

---

## 🏗️ 7. The Full Navigation Stack

```text
LiDAR → SLAM → Localization → Map → A* (global) → Obstacle avoidance (local) → Motors
```

---

## ⚠️ 8. Common Mistakes

- **Thinking SLAM is navigation.** SLAM builds the map; planning uses it.
- **Thinking A* and Dijkstra are unrelated.** A* *is* Dijkstra plus a
  heuristic.
- **Forgetting dynamic obstacles.** A path is not computed once and obeyed
  forever.
- **Using an inadmissible heuristic** and wondering why paths are suboptimal.
- **Planning on a map that is already wrong** — remember Lesson 27: a drifted
  map produces a confident plan straight into a wall.

---

## 🎯 9. Interview Questions

**Q: Why is A\* more popular than Dijkstra?**

> A* uses a heuristic to search in the direction of the goal, so in most
> practical cases it is faster than Dijkstra while still finding the shortest
> path.

<details>
<summary>Q: When would you deliberately use Dijkstra instead?</summary>

When there is no meaningful heuristic — for example on a road network where
travel cost is time rather than distance, and traffic makes straight-line
distance a poor guess. Dijkstra is also the right choice when you need the
shortest path from one point to *every* other point, since A* is optimised for
a single goal.
</details>

<details>
<summary>Q: What happens if the heuristic is set to zero?</summary>

A* becomes Dijkstra exactly. `cost + 0` is just `cost`. This is the clearest
way to see that they are one algorithm with a parameter — try it in the demo by
making `heuristic()` return 0, and the explored-cell count rises to Dijkstra's.
</details>

---

## 🧠 Mini Challenge

```text
S . X . G
. . X . .
. . . . .
```

Can the robot go straight? **No** — an obstacle is in the way, so the planner
routes around it, down through the free rows and back up.

**Then try this:** in `path_planning_demo.py`, make `heuristic()` return `0`
and re-run. A* will examine exactly as many cells as Dijkstra. That single
change is the entire difference between the two algorithms.

---

## 💡 10. Industry Architecture

```text
Sensors → Sensor fusion → Localization → SLAM
   → Global planner → Local planner → Obstacle avoidance → Motor control
```

---

## 🚀 Next — Lesson 29: Computer Vision for Robotics

The robot can now move, map, and plan. But it still does not know whether the
thing in front of it is **a person, a bottle, a chair, or a dog**.

> **Note:** we already covered much of this ground in Lessons 13–16 — pixels,
> RGB vs grayscale, OpenCV, and YOLO, with runnable demos. Lesson 29 could
> either recap briefly and go deeper (object tracking, following), or move
> straight to a **vision-based object follower** as the mini capstone.
