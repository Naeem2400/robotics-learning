# Lesson 16 — YOLO (You Only Look Once)

**Module 9 — AI Vision**

> **Golden rule:** The camera *sees*. YOLO *recognises*. The robot *acts*.

That is the core workflow of modern AI robotics.

---

## 📖 1. Theory — What Is YOLO?

### Technical definition

**YOLO (You Only Look Once)** is a **real-time object detection model** that
finds objects in an image or video *and* reports where they are.

### In plain terms

Walking down a road, you take in a car, a person, a traffic light, and a
bicycle — all in a single glance. Your brain identifies everything at once.

YOLO works the same way. Hence the name: it looks at the image **once** and
detects everything in it.

---

## 🧠 2. Why YOLO Changed Everything

Older detectors worked by sliding a window across the image and asking "is
there an object here?" thousands of times per frame. Accurate, but far too slow
for a moving robot.

YOLO looks at the whole image **one time** and predicts every box in a single
pass. That change took detection from a few frames per second to real time —
which is what made vision usable on robots and cars at all.

> **Connect to Lesson 13:** we said FPS is the *sense* half of the Sense →
> Think → Act loop. YOLO is what made the *think* half fast enough to keep up.

---

## 🌍 3. Real World Example

A warehouse robot's camera captures a scene containing a box, a worker, and a
chair. YOLO returns:

```text
person  99%
box     98%
chair   97%
```

The robot decides: **"do not go near the worker."**

### The complete pipeline

```text
Camera → OpenCV → YOLO → Detected objects → Robot brain → Movement
```

---

## 📦 4. Bounding Boxes

YOLO draws a rectangle around each object it finds:

```text
+---------------------------+
|                           |
|     ┌───────────┐         |
|     │  PERSON   │  99%    |
|     └───────────┘         |
|                           |
+---------------------------+
```

That rectangle is a **bounding box**. For every detected object you get:

| Field | Example |
|---|---|
| Label | `person` |
| Confidence | `98%` |
| Position | `x = 250, y = 180` |

The position is what makes detection *useful*. "There is a bottle somewhere in
this image" cannot guide an arm. "There is a bottle at (170, 162)" can.

---

## 🎯 5. Confidence Score

Confidence is how sure the model is:

```text
bottle  99%   -> very sure
cat     52%   -> not sure at all
```

Robots act on a **threshold**:

```python
if confidence > 0.80:
    pick_object()
else:
    ignore()
```

### Choosing the threshold is a real engineering decision

- **Too low** → the robot reacts to things that are not there (jumpy, unsafe)
- **Too high** → the robot misses real objects (blind, useless)

There is no universally correct value. A safety-critical system uses a low
threshold *for humans* (better a false alarm than a missed person) and a high
threshold for objects it wants to grab.

---

## 💻 6. Practical

### The real YOLO code

```bash
pip install ultralytics
```

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")        # a small, fast model
results = model("image.jpg")
results[0].show()
```

What happens inside:

```text
Image → resize → neural network → boxes + labels + confidence → output
```

> **⚠️ Note on installing:** `ultralytics` pulls in PyTorch, which is a very
> large download (hundreds of MB). On a slow connection this takes a long time.
> The demo below teaches the same concepts and needs **no installation**.

### Run this now — no install needed

```bash
python3 detection_demo.py
```

[`detection_demo.py`](../detection_demo.py) takes detections in exactly the
format YOLO returns, applies the confidence threshold, draws the bounding
boxes into a PNG, and prints the robot's decision:

```text
  ACCEPT  person     99%  box=( 30, 60)-(110,220)  centre=( 70,140)
  ACCEPT  bottle     96%  box=(150,120)-(190,205)  centre=(170,162)
  REJECT  cat        52%  box=(130, 20)-(175, 60)  centre=(152, 40)

  A person was detected -> stop and keep a safe distance.
```

**When you install ultralytics later, the only thing that changes is where the
detections come from.** The threshold logic and the robot decision stay exactly
as they are — which is the point of the exercise.

---

## 🏢 7. Industry Examples

| Company | Detects |
|---|---|
| **Tesla** | Cars, pedestrians, traffic signs, road lines |
| **Amazon Robotics** | Packages, workers, shelves, barcodes |
| **Figure AI** | Hands, cups, bottles, humans, furniture |

### YOLO versions

YOLOv5 → YOLOv8 → YOLOv9 → YOLOv10 → YOLO11 …

**Version numbers keep changing; the concept does not.** Learn the concepts —
bounding box, confidence, threshold, real-time detection — rather than
memorising versions. A new model will be out before you finish the course, and
your understanding will transfer to it unchanged.

---

## ⚠️ 8. Limitations and Common Mistakes

YOLO is not perfect. It makes mistakes with:

- Darkness
- Fog or rain
- Partly hidden objects
- Reflections and glass

This is why real robots combine **camera + LiDAR + depth camera + IMU**.

> **Never depend on a single sensor or a single AI model in real robotics.**
> You have seen this twice now — the table that our 2D lidar could not see in
> Lesson 10, and sensor fusion in Lesson 12. Same lesson, third time.

**Common mistakes:**

- Thinking OpenCV *is* AI — it is not; it prepares images for AI
- Trusting a detection without checking its confidence
- Testing only on clean, bright, straight-on images
- Assuming detection tells you distance — **it does not.** A bounding box is
  2D. Knowing how far away an object is needs depth, stereo, or lidar.

---

## 🎯 9. Interview Questions

**Q: What is the difference between YOLO and OpenCV?**

> OpenCV processes images. YOLO detects objects inside them.

<details>
<summary>Q: Why is it called "You Only Look Once"?</summary>

Earlier detectors examined an image many times — sliding a classifier across
thousands of candidate regions. YOLO passes the whole image through the network
a single time and predicts all boxes at once. That single pass is what makes it
fast enough for real-time robotics.
</details>

<details>
<summary>Q: A detection comes back at 55% confidence. What should the robot do?</summary>

It depends entirely on the cost of being wrong. For an object to pick up,
ignore it — acting on a coin-flip wastes time and may damage something. For a
*human* in the robot's path, 55% is more than enough to stop: the cost of a
false alarm is a brief pause, while the cost of a miss is an injury.
Thresholds should reflect consequences, not a single global number.
</details>

---

## 🛣️ The Three Tracks From Here

```text
Track 1 - Programming & Software    Python → ROS 2 → AI
Track 2 - Electronics & Hardware    Arduino → ESP32 → Sensors
Track 3 - AI & Computer Vision      OpenCV → YOLO → LLMs → Agentic AI
```

These three eventually combine into one intelligent robot.

---

## 🚀 Next — Lesson 17

**ROS 2 — the operating system of robotics.** What it is, why every robotics
company uses it, what nodes and topics are, publishers and subscribers, and how
the different parts of a robot talk to each other.

This is the turning point: once ROS 2 makes sense, professional robotics
software architecture starts making sense too.
