# Lesson 43 — Depth Estimation & 3D Vision

**Module 17 — AI Vision**

> The robot can see a cup and even trace its exact shape. But it still cannot
> answer the one question a robot arm must have: **how far away is it?**

---

## 🎯 Lesson Goal

- What depth is, and 2D vs 3D vision
- Stereo vision and monocular depth
- RGB vs RGB-D cameras
- Depth maps and point clouds
- Intel RealSense, Luxonis OAK-D, Depth Anything V2

---

## 📖 The Problem

YOLO says *"that is a cup."* Segmentation says *"here is its exact outline."*
Neither says **"it is 42 cm away."** Without distance, a robot arm reaching for
the cup either stops short or drives through it.

### Why humans have two eyes

You can see with one eye, but you judge **distance** with two. Each eye sees a
slightly different view; your brain measures the difference and infers depth.
Robotics copies this exactly — it is called **stereo vision**.

| | 2D vision | 3D vision |
|---|---|---|
| Sees | colour image | colour **+ distance** |
| Cup | "a cup" | "a cup, 42 cm away" |
| Enough for | recognition | **grasping, navigation** |

---

## 🔬 Practical — Depth From Two Eyes, No Sensor

```bash
source .venv/bin/activate

python depth_estimation.py --test               # a sample stereo pair
python depth_estimation.py --pair L.jpg R.jpg   # your own rectified pair
```

[`depth_estimation.py`](../depth_estimation.py) takes **two photos of the same
scene from slightly different positions** and recovers depth using only
geometry — no depth sensor, no AI model. Verified output:

```text
  stereo pair: 1282 x 1110
  disparity: 0.6 .. 111.0 px (bigger = closer)
    nearest  disparity  111.0 px -> ~ 0.38 m away
    median   disparity   59.8 px -> ~ 0.70 m away
    far      disparity    0.6 px -> ~74.67 m away
```

It saves `output_depth.jpg`: the photo beside a colour depth map where **warm =
near, cool = far**. On the sample, the plant in front glows warm and the
wallpaper behind is cool — exactly the depth your own eyes perceive.

### The one equation

Depth comes from **disparity** — how far a point shifts between the left and
right image:

```python
depth = (focal_length * baseline) / disparity
```

It is an **inverse** relationship, and that is the whole intuition:

- A **near** object shifts a lot between the two views → **big** disparity →
  small distance.
- A **far** object barely shifts → **tiny** disparity → large distance.
- Something infinitely far has zero disparity.

Hold a finger close and blink each eye — it jumps a lot. A distant wall barely
moves. That jump *is* disparity.

---

## 🎨 Depth Map vs Point Cloud

A **depth map** is an image where each pixel's value is its distance — the
colour picture the demo saves.

A **point cloud** is the 3-D version: every pixel becomes a dot with real
`(x, y, z)` coordinates in space. That cloud of dots **is** the robot's model
of the world — what it plans paths and grasps through. Depth map → point cloud
is a straightforward projection once you know the camera's optics.

---

## 📷 How Robots Actually Get Depth

| Method | How | Trade-off |
|---|---|---|
| **Stereo** (this demo) | Two cameras, compare views | Needs texture; struggles on blank walls |
| **RGB-D camera** | Projects a pattern / times light | Direct depth; indoor range limits |
| **LiDAR** | Times laser pulses | Precise, long range; expensive |
| **Monocular AI** | One image, a model *guesses* depth | No extra hardware; an estimate, not a measurement |

### The hardware you will meet

- **Intel RealSense** — RGB-D camera; depth, colour, sometimes an IMU. Common on
  robot arms and mobile robots.
- **Luxonis OAK-D** — stereo depth **plus on-device AI**, so detection and depth
  run in the camera itself.
- **Depth Anything V2** — an AI model that estimates depth from a *single* RGB
  image. Impressive, and needs no special camera — but it is a **guess**, and a
  large download. For safety-critical grasping, a real depth sensor is trusted
  over an estimate.

> This lesson uses **stereo** for the practical because it needs no model
> download and the maths is transparent. Monocular AI depth is a great next
> experiment when you have the bandwidth for the model.

---

## 🏗️ Where Depth Fits

```text
RGB camera → YOLO (what) → segmentation (exact shape)
   → depth (how far) → point cloud → grasp / navigation planning → robot
```

| Robot | Uses depth to |
|---|---|
| Robot arm | Know how far to reach for a grasp |
| Self-driving car | Measure distance to a pedestrian, then brake |
| Drone | Avoid a tree at the right moment |
| Home robot | Steer around a chair 80 cm away |

---

## ⚠️ Common Mistakes

- **Thinking YOLO gives distance.** It gives class and 2-D location, never
  depth.
- **Confusing an RGB camera with an RGB-D camera.** Different hardware; a laptop
  webcam has no depth.
- **Thinking a point cloud is an image.** It is a 3-D set of points.
- **Trusting monocular AI depth as a measurement.** It is an estimate; scale can
  be wrong.
- **Expecting stereo to work on a blank wall.** With no texture, there is
  nothing to match between the two views.

---

## 🎯 Interview Questions

**Q: Why does a robot arm need a depth camera?**

> To know an object's exact distance and 3-D position, so it can plan an
> accurate reach and grasp. A 2-D detection gives direction but not distance.

<details>
<summary>Q: Why is the disparity-to-depth relationship inverse?</summary>

Because a nearby object subtends a larger angle difference between the two
cameras than a distant one, so it shifts more pixels between the images. Depth
is `focal × baseline / disparity`: as disparity shrinks toward zero (a far
object), depth grows toward infinity. This is also why stereo loses precision
at long range — beyond some distance the disparity change per metre is smaller
than one pixel.
</details>

---

## 🧠 Mini Challenge

A cup reads **35 cm** away. What does the robot now know?

> Its distance — so it can compute exactly how far the arm must extend to reach
> it. Run the demo and read the per-region distances the script prints.

---

## 🎥 Reel Idea

**"How Do Robots Know Distance?"** — show the plant photo, then the warm/cool
depth map beside it, and the line *"nearest: 0.38 m, background: 74 m — from two
photos, no sensor."* End: *"This is how a robot reaches for the right thing."*

---

## 🏆 Portfolio Project

**AI Depth Estimation System** — stereo depth from an image pair, a colour depth
map, per-object distances, and (as an upgrade) a monocular AI depth comparison.
The distance numbers make it read as robotics, not just a pretty heatmap.

---

## 💻 Software-First Path (no hardware yet)

On a MacBook Air M1 you can learn the whole stack before buying a sensor:

1. Webots — simulation 2. OpenCV — camera processing 3. YOLO — detection
4. Depth Anything V2 — AI depth 5. Open3D — visualise point clouds
6. ROS 2 + Gazebo — the full stack

When you later buy a RealSense or OAK-D, the concepts will already be yours.

---

## 🚀 Next — Lesson 44: SLAM

The robot can now see, track, and measure distance. Next it answers *"where am
I, and what does this place look like?"* — building a map of an unknown room
with no GPS. LiDAR SLAM, visual SLAM, and the ROS 2 navigation stack.

> We already met SLAM's core idea in [Lesson 27](lesson-27-slam.md) with a
> runnable occupancy-grid demo — Lesson 44 goes deeper into the real ROS 2
> tools.
