# Lesson 36 — Object Tracking & Object Following

**Module 17 — AI Vision**

> The robot can already **detect** a bottle. But if the bottle moves, the robot
> just watches. Today it learns to **follow**.

---

## 🎯 Lesson Goal

- Object detection vs object tracking
- Object following
- Object centre vs camera centre
- The basic idea of PID
- Robot movement logic

---

## 📖 Detection vs Tracking

| Detection | Tracking |
|---|---|
| Finds objects in **each frame independently** | Follows the **same** object across frames |
| "There is a person" | "This is person **#3**, the same one as last frame" |
| No memory | Keeps identity |

Detection alone has no idea that the bottle in frame 2 is the same bottle from
frame 1. Tracking assigns each object a **persistent ID**.

### Verified on this machine

```text
  frame 0: 4 person(s), track IDs = [1, 2, 3, 4]
  frame 1: 4 person(s), track IDs = [1, 2, 3, 4]
  frame 2: 3 person(s), track IDs = [1, 2, 3]     <- one was briefly missed
  frame 3: 4 person(s), track IDs = [1, 2, 3, 4]
```

Look closely at frame 2: detection **flickered** and lost someone for a moment,
but the IDs of the others stayed stable. That is exactly why tracking matters —
a robot following "person #3" is not confused by a single dropped frame, whereas
a robot following "the third box in this frame's list" would jump to the wrong
person instantly.

---

## 🧭 The Core Idea — Just Two Numbers

Following a target needs only the **object's centre** and the **camera's
centre**.

For a 640×480 camera, the centre is `x = 320`.

If YOLO reports a box from `x = 100` to `x = 220`, the object's centre is:

```text
(100 + 220) / 2 = 160
```

160 is left of 320, so the object is **left** of the robot.

| Object centre | vs camera centre | Robot action |
|---|---|---|
| 90 | far left | ⬅ **Turn left** |
| 540 | far right | ➡ **Turn right** |
| 320 | dead on | ⬆ **Forward** |
| — | not visible | ⏹ **Stop / search** |

```python
if object_x < 280:
    turn_left()
elif object_x > 360:
    turn_right()
else:
    move_forward()
```

That is genuinely the whole algorithm.

---

## 🔬 Practical — Watch the Robot Decide

```bash
source .venv/bin/activate

python object_follower.py --test              # decision logic, no camera
python object_follower.py                     # follow a bottle
python object_follower.py --target person     # follow a person
```

[`object_follower.py`](../object_follower.py) draws the camera centre line, the
dead zone, and the live decision on screen. Move a bottle around and watch it
switch between `TURN LEFT`, `TURN RIGHT`, `FORWARD` and `BACK UP`.

Verified output of the logic:

```text
  object at x= 90, size  10% -> TURN LEFT  (offset -230)
  object at x=320, size  10% -> HOLD       (offset +0)
  object at x=540, size  10% -> TURN RIGHT (offset +220)
  object at x=320, size  35% -> BACK UP    (offset +0)
  object at x=320, size   2% -> FORWARD    (offset +0)
```

> **Note:** the first run may auto-install `lap`, a small dependency the
> tracker needs. Let it finish, then run again.

### Two details worth understanding

**1. The dead zone.** The robot only turns when the object is more than 60 px
off-centre. Without that band it would twitch left-right-left forever as the
detection jitters by a pixel. This is the same **hysteresis** idea as the
obstacle avoider in Lesson 26 — a recurring pattern in real control code.

**2. Box size as a distance sensor.** A camera cannot measure distance, but a
*bigger box means closer*. The script uses the box area as a rough stand-in:
over 25% of the frame → back up; under 4% → approach. It is crude but it works,
and it is what you do when you have no depth sensor.

---

## 🎛️ PID — the Next Problem

Our robot turns at a **fixed speed** regardless of how far off-target it is.
Barely off-centre? Full turn. Way off? Also full turn.

The result is overshoot: the robot swings past the target, then swings back,
oscillating forever.

A **PID controller** fixes this by making the correction **proportional to the
error**:

```text
small error  ->  gentle turn
large error  ->  hard turn
```

That single change ("P", the proportional term) removes most of the wobble. The
I and D terms refine it further. We will cover this properly later — for now,
know **why** it exists: fixed-speed corrections always overshoot.

---

## 🔀 Tracking Algorithms

YOLO handles detection; a separate tracker maintains identity:

| Tracker | Notes |
|---|---|
| **ByteTrack** | Fast, the sensible default — what our script uses |
| **BoT-SORT** | More robust through occlusion |
| DeepSORT / StrongSORT / OC-SORT | Older or heavier options |

```python
model.track(frame, persist=True, tracker="bytetrack.yaml")
```

⚠️ **`persist=True` is essential.** Without it, tracker state resets every call
and IDs are reassigned each frame — you get detection wearing a tracking
costume.

---

## 🌍 Real Applications

| Robot | Follows |
|---|---|
| Airport robot | A passenger |
| Hospital robot | A nurse |
| Warehouse robot | A worker |
| Shopping robot | A customer |
| Smart suitcase | Its owner |

Every one of these is the code above, plus motors.

```text
Camera → YOLO → tracking → centre → PID → motor controller → robot
```

---

## ⚠️ Common Mistakes

- **Treating each frame as a new object** — use tracking IDs.
- **Thinking detection is following.** Detection tells you *what*; following
  needs *where relative to me*, and an action.
- **Forgetting the dead zone** — the robot twitches endlessly.
- **Fixed-speed turning** — causes overshoot; see PID.
- **Following the wrong instance** when several are visible. Our script follows
  the **largest** box, i.e. the nearest one.

---

## 🎯 Interview Questions

**Q: What is the difference between detection and tracking?**

> Detection identifies objects in a single frame. Tracking follows an object's
> movement across frames and maintains its identity with a persistent ID.

<details>
<summary>Q: Why is tracking usually faster than running detection every frame?</summary>

Detection searches the entire image for every object, every time. A tracker
already knows roughly where the object was and how it was moving, so it only
has to look nearby and match candidates to existing tracks. Many production
systems run full detection only every N frames and track in between, which cuts
compute dramatically while keeping smooth output.
</details>

---

## 🧠 Mini Challenge

Camera centre `320`, bottle centre `90` — what does the robot do?

> ⬅ **Turn left.** 90 is 230 px left of centre, far beyond the dead zone.

The script prints exactly this: `TURN LEFT (offset -230)`.

**Then experiment:** set `DEAD_ZONE = 5` and run it. The robot becomes jittery,
flipping decisions constantly. Set it to `250` and it barely reacts at all.
Tuning that number *is* the engineering.

---

## 🎥 Reel Idea

**"My AI Robot Can Follow Objects 🤖"** — the on-screen HUD does the work for
you: move the bottle left, the label flips to `TURN LEFT`; move it right, it
flips to `TURN RIGHT`. The decision changing live as you move your hand is the
whole story, and it needs no explanation.

---

## 🚀 Next — Lesson 37: Pose Estimation

The robot moves beyond boxes to detecting a person's **head, shoulders, elbows,
wrists, hips, knees and feet** — the technology behind fitness apps, sports
analytics, gesture control, humanoid robots, and motion capture.

---

## 🎯 Mentor Habit

After every AI vision project, answer these five:

1. What problem does this solve?
2. How would it be used in a warehouse, hospital, farm, or home robot?
3. How would it connect to an ESP32, Raspberry Pi, or Jetson?
4. What is its GitHub portfolio version?
5. How could it become a commercial product for a client?
