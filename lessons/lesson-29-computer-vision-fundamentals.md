# Lesson 29 — Computer Vision Fundamentals

**Module 16 — Computer Vision for Robotics**

> Earlier robots only *sensed*. Today's robots **see and understand**.

---

## 📚 What You Already Know

Much of this ground is covered, with runnable code:

| Topic | Lesson | Demo |
|---|---|---|
| Pixels, resolution, RGB vs grayscale | [Lesson 13](lesson-13-camera.md) | [`pixels_demo.py`](../pixels_demo.py) |
| An image is a matrix of numbers | [Lesson 15](lesson-15-how-a-robot-sees.md) | [`see_like_a_robot.py`](../see_like_a_robot.py) |
| OpenCV operations | [Lesson 14](lesson-14-opencv.md) | [`image_analyzer.py`](../image_analyzer.py) |
| YOLO, boxes, confidence | [Lesson 16](lesson-16-yolo.md) | [`detection_demo.py`](../detection_demo.py) |

**This lesson consolidates that and adds the piece not yet covered: the
difference between traditional and AI vision, and why it matters.**

---

## 🎯 Quick Recap

```text
Camera → Image → Computer Vision → AI Decision → Robot Action
```

| Human | Robot |
|---|---|
| Eyes | Camera |
| Brain | AI model |
| Decision | Robot controller |

- A **pixel** (picture element) is the smallest unit of an image
- **Resolution** is how many pixels there are: 640×480, 1920×1080, 4K
- **RGB** stores 3 numbers per pixel; **grayscale** stores 1 — three times
  less data, which is why many pipelines drop colour first
- **OpenCV** is the library that processes images; it is **not** AI

---

## ⭐ The New Idea — Rules vs Learning

### Traditional computer vision

A programmer writes the rules:

```text
if colour == red  ->  object = apple
```

### AI vision

The model is shown thousands of labelled examples and works out the pattern
itself.

That sounds like a small difference. It is not.

---

## 🔬 Practical — Watch Rules Fail

```bash
python3 traditional_vs_ai_vision.py
```

[`traditional_vs_ai_vision.py`](../traditional_vs_ai_vision.py) writes one
perfectly reasonable rule:

```python
if r > 200 and g < 80 and b < 80:   # this pixel is red
```

...and then tests it on five images.

| Image | Rule says | Reality | |
|---|---|---|---|
| Red apple, good light | APPLE | apple | ✅ |
| **Same apple, dim light** | no apple | apple | ❌ |
| **Same apple, in shadow** | no apple | apple | ❌ |
| **Green apple** | no apple | apple | ❌ |
| **Red rubber ball** | APPLE | not an apple | ❌ |

### Score: 1 out of 5

Look at what failed. Images 2 and 3 are the **exact same apple** — only the
lighting changed, and every number in the image changed with it (the point made
in Lesson 15). Image 4 is an apple that was never red. Image 5 is red but is
not an apple at all.

### Why this cannot be patched

You could add a rule for dim light. Then someone photographs an apple at
sunset. Add another. Then a tomato appears. Add another. **This never ends** —
the real world has more cases than you can enumerate.

An AI model is never given the rule. It sees thousands of labelled apples —
bright, dim, red, green, partly hidden — and learns what they share.

> ### ⚠️ But rules are not obsolete
>
> If your robot watches one factory conveyor under fixed lighting, a colour
> rule is **faster, simpler, and needs no training data or GPU**. Choosing
> between them is an engineering decision, not a fashion. A good engineer asks
> *"how much does my environment vary?"* before reaching for a neural network.

---

## 🏗️ The Modern Pipeline

```text
Camera → OpenCV → YOLO → Object detection → ROS 2 → Robot action
```

| Robot | Pipeline |
|---|---|
| **Warehouse** | Camera → YOLO → box detected → pick → deliver |
| **Tesla** | Cameras → vision AI → lane + pedestrian detection → drive |
| **Humanoid** | Camera → face detection → recognise person → speak → move |

---

## ⚠️ Common Mistakes

- **Thinking OpenCV is AI.** OpenCV is a library for processing images; the
  model that recognises things is separate.
- **Confusing RGB with resolution.** RGB is *channels per pixel*; resolution is
  *how many pixels*.
- **Assuming every vision problem needs AI.** Sometimes a colour threshold is
  the correct answer — see the box above.
- **Testing only on ideal images.** The demo above is the whole argument.

---

## 🎯 Interview Questions

**Q: What is the difference between OpenCV and YOLO?**

> OpenCV is a computer vision library used for image processing and camera
> operations. YOLO is an AI model that detects objects in images. They are
> normally used together — OpenCV prepares the frame, YOLO interprets it.

<details>
<summary>Q: When would you choose classical CV over a neural network?</summary>

When the environment is controlled and the task is simple: fixed lighting, a
known background, a specific colour or shape. Classical methods run in
microseconds on a CPU, need no training data, and fail predictably. A neural
network is worth its cost when the input varies in ways you cannot enumerate —
lighting, angle, occlusion, unfamiliar objects. Many production robots use
both: classical CV to preprocess and cheaply reject frames, a model for the
hard decisions.
</details>

---

## 💡 2026 Industry Trend

```text
RGB camera + depth camera + thermal camera
      ↓
OpenCV
      ↓
YOLO / Vision Transformer (ViT)
      ↓
3D scene understanding
      ↓
LLM reasoning
      ↓
Robot action
```

Modern robots do not merely *see* — they try to understand a scene
**semantically**: not "a red region at (170, 162)" but "a mug, on a table,
within reach."

---

## 🚀 Next — Lesson 30: OpenCV Practical

Using the MacBook camera: install OpenCV, open the camera, view a live video
stream, save images, record video, and control it from the keyboard.

> **⚠️ Two things to sort out first.**
>
> 1. **OpenCV is not installed yet.** Attempts stalled repeatedly on this
>    connection (see Lesson 14). A better network — or Docker — is needed
>    before the practical can run.
> 2. **Camera access needs macOS permission.** The first time a script opens
>    the camera, macOS shows a prompt; if it is denied, `cv2.VideoCapture(0)`
>    returns empty frames with **no error message**. Check
>    *System Settings → Privacy & Security → Camera*.
