# Lesson 42 — Multi-Object Tracking (MOT)

**Module 17 — AI Vision**

> Ten people walk through a room. Which one is the person the robot saw a
> moment ago? Detection cannot answer that. **Tracking** can.

---

## 🎯 Lesson Goal

- What multi-object tracking is
- Detection vs tracking
- Object IDs and the track lifecycle
- ByteTrack, BoT-SORT, DeepSORT
- Robotics applications

---

## 📖 The Problem

YOLO detects three people in frame 1: `person`, `person`, `person`. In frame 2
it detects three people again. But it has **no idea** the first person in frame
2 is the same as the first in frame 1 — each frame is independent.

**Tracking** fixes this by giving every object a **persistent ID**:

```text
frame 1:  woman #1   man #2   child #3
frame 2:  woman #1   man #2   child #3   <- same IDs
```

Now the robot knows these are the same people.

| Detection | Tracking |
|---|---|
| Finds objects, each frame alone | Follows the same object across frames |
| No memory | Uses previous frames |
| No IDs | Persistent unique IDs |

---

## 🔬 Practical — Two Views of the Same Idea

### The real one: YOLO + ByteTrack

```bash
source .venv/bin/activate

python multi_object_tracking.py --test                    # verify IDs persist
python multi_object_tracking.py                           # built-in camera
python multi_object_tracking.py --url http://IP:8080/video   # phone camera
python multi_object_tracking.py --follow 1                # highlight only ID 1
```

[`multi_object_tracking.py`](../multi_object_tracking.py) uses YOLO's built-in
ByteTrack. Each object gets a coloured box, an ID, and a short motion trail.
Verified output:

```text
    frame 0: track IDs = [1, 2, 3, 4]
    frame 1: track IDs = [1, 2, 3, 4]
    frame 2: track IDs = [1, 2, 3]        <- ID 4 briefly lost
    frame 3: track IDs = [1, 2, 3]
    frame 4: track IDs = [1, 2, 3, 4]     <- and recovered, SAME ID
    frame 5: track IDs = [1, 2, 3, 4]
```

Look at ID 4: detection dropped it for two frames, then it came back with the
**same ID**. That is **re-identification** — the tracker held the identity
through a brief disappearance. A robot following "person #4" is not fooled.

### The transparent one: a tracker from scratch

Production uses ByteTrack, but the core algorithm fits in ~60 lines.
[`simple_tracker.py`](../simple_tracker.py) implements it with no dependencies:

```text
  frame 0: 2 detections -> IDs seen [1, 2]
  frame 2: 3 detections -> IDs seen [1, 2, 3]    <- new object, new ID
  frame 3: 2 detections -> IDs seen [1, 3]       <- object 2 vanished...
  frame 5: 2 detections -> IDs seen [1, 3]          ...track kept alive...
  frame 6: 2 detections -> IDs seen [1, 3]          ...then dropped (alive: [1,3])
```

Its three rules **are** tracking:

1. **Match** each detection to the nearest existing track.
2. **Create** a new track (new ID) for anything that matches nothing.
3. **Age out** a track that goes unmatched for several frames.

---

## ♻️ The Track Lifecycle

That third rule is the **track lifecycle**, and it is the heart of MOT:

```text
detected → tracked (age 0) → missed (age 1) → missed (age 2) → ... → removed
                 ↑______ seen again: back to age 0 ______|
```

- **New object** → new ID.
- **Seen each frame** → ID stays, age stays 0.
- **Briefly hidden** → track survives a few frames (so an ID is not lost to one
  bad frame or a person stepping behind a door).
- **Gone for good** → track removed after `max_age` misses.

Set `max_age` too low and IDs flicker every time detection stutters. Too high
and a departed person's ID lingers and gets stolen by a newcomer. Choosing it
is real tuning — the same trade-off as the dead zone in Lesson 36.

---

## 🔀 The Algorithms

| Tracker | Notes |
|---|---|
| **ByteTrack** | Fast, accurate, real-time — the sensible default; what our demo uses |
| **BoT-SORT** | Stronger in crowds and with a moving camera |
| **DeepSORT** | Older; adds appearance features to survive longer occlusions |

Under the hood these use a **Kalman filter** (predict where each object will be
next) and the **Hungarian algorithm** (optimally match predictions to
detections). Our `simple_tracker.py` replaces both with "nearest within a
threshold" — cruder, but the same shape. Those two algorithms are the homework.

---

## 🤖 Why IDs Matter to a Robot

The whole point: a robot can act on a *specific* object.

```text
Home robot: follow ID 1 (the owner), ignore ID 2 (a guest)
Warehouse:  track worker #2, keep a safe distance
Airport:    guide passenger #12 to the gate
Self-driving: track pedestrian #5, predict the crossing, brake
```

The `--follow 1` flag demonstrates exactly this — it highlights one ID and dims
everyone else.

---

## ⚠️ Tracking Challenges

- **Occlusion** — a person steps behind a door. A good tracker keeps the ID
  ready and resumes it on reappearance (the lifecycle above).
- **Fast motion** — the object moves farther between frames than the match
  threshold, so it looks like a new object. A Kalman filter *predicts* the
  motion to cope.
- **Similar appearance** — two people in the same clothes confuse
  appearance-based trackers; motion prediction helps disambiguate.

---

## 🎯 Interview Questions

**Q: Difference between detection and multi-object tracking?**

> Detection identifies objects in each frame independently. MOT maintains each
> object's identity across frames, assigning a persistent unique ID.

<details>
<summary>Q: Why keep a track alive for several frames after the object disappears?</summary>

Because detection is noisy and objects get briefly occluded. If a track were
deleted the instant one frame missed it, every stutter or passing obstruction
would end the ID — and the object would return as a *new* ID, breaking any
"follow this specific person" behaviour. A short grace period (`max_age`) lets
the same identity resume when the object reappears. The cost is that a truly
departed object lingers briefly, so the value is a tuned trade-off.
</details>

---

## 🧠 Mini Challenge

Frame 1: a person has `ID 3`. Frame 2: the person moves left. What is the ID?

> **Still `ID 3`.** The whole purpose of tracking is that the ID does not change
> as the object moves. Confirm it: run `--test` and watch the IDs hold.

---

## 🎥 Reel Idea

**"How Does a Robot Remember People?"** — two people walk across frame, each
with a coloured `ID 1` / `ID 2` box and a motion trail. They cross paths, walk
around, and the IDs stay put. End on `--follow 1`: one person stays highlighted,
the other dims. *"This is multi-object tracking."*

---

## 🏆 Portfolio Project

**AI Multi-Object Tracking System** — live tracking, persistent IDs, motion
trails, a follow-one-ID mode, and an FPS readout. Record it with your phone
camera (`--url`) for a crisp 1080p demo.

---

## 📚 Homework — Overview Only

1. ByteTrack 2. BoT-SORT 3. **Kalman filter** (predict next position)
4. **Hungarian algorithm** (optimal matching) 5. Re-identification (ReID)

Kalman and Hungarian look intimidating; do not worry — we cover them later with
simple examples. `simple_tracker.py` is already a stripped-down stand-in for
both.

---

## 🚀 Next — Lesson 43: Depth Estimation

The robot can see and track — but not yet judge **how far away** things are.
Monocular depth, stereo vision, RGB-D cameras (Intel RealSense, Luxonis OAK-D),
and Depth Anything V2 — turning a 2-D image into a 3-D understanding of the
world.
