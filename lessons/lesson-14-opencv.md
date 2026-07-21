# Lesson 14 — OpenCV: The Foundation of Robot Vision

**Module 8 — OpenCV**

---

## 📖 1. Theory — What Is OpenCV?

### Technical definition

**OpenCV (Open Source Computer Vision Library)** is an open-source library for
processing images and video.

### In plain terms

OpenCV is the robot's **vision toolkit**:

- The **camera** only takes the image
- **OpenCV** processes and prepares that image
- **AI** understands it

---

## 🧠 2. Why Does OpenCV Exist?

A camera hands you millions of raw numbers. Almost none of them matter.

A robot that must decide in 1/30th of a second cannot afford to examine every
pixel of a 12-megapixel photo. OpenCV exists to **throw away what does not
matter, fast** — shrink the image, drop the colour, remove the noise, keep only
the edges — so the AI model receives a small, clean input.

Put simply: **OpenCV is how a robot turns "too much data" into "just enough."**

---

## 🌍 3. Real World Example

You have a photo and you want to resize it, rotate it, crop it, or detect a
face in it. OpenCV does all of these.

The standard robot pipeline:

```text
Camera → OpenCV → Processed image → AI model → Decision → Robot
```

Almost every AI robot follows this flow.

---

## 🏢 4. Industry Examples

| Company | Pipeline |
|---|---|
| **Amazon warehouse robot** | Camera → OpenCV → barcode read → AI → robot drives to shelf |
| **Tesla** | Camera → image processing → AI → steering |
| **Hospital robot** | Camera → OpenCV → patient detected → navigation |

---

## 💻 5. Practical — Installation

### Step 1 — Check Python

```bash
python3 --version
```

### Step 2 — Create a virtual environment

A virtual environment keeps this project's packages separate from the rest of
your system, so one project can never break another.

```bash
python3.13 -m venv .venv
```

> **Why `python3.13` and not plain `python3`?** On this machine `python3` is
> version 3.14, which is so new that OpenCV does not publish a ready-made
> package for it yet — pip would try to build it from source and fail. Python
> 3.13 has a prebuilt package. **This is a real robotics skill:** the newest
> version is often not the usable one.

### Step 3 — Activate it

```bash
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`.

### Step 4 — Install OpenCV

```bash
pip install opencv-python matplotlib
```

### Step 5 — Verify

```bash
python -c "import cv2; print(cv2.__version__)"
```

If a version number prints — congratulations 🎉 OpenCV is installed.

---

### ⚠️ A note for macOS users

The classic OpenCV display code is:

```python
cv2.imshow("Robot Vision", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

On macOS this is often unreliable — window focus and permissions get in the
way. This course uses two approaches that work everywhere instead:

**Save the file and open it** (used by our mini project):

```python
cv2.imwrite("output.png", image)
```

**Or display with Matplotlib:**

```python
import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)   # BGR -> RGB, see below

plt.imshow(image)
plt.axis("off")
plt.show()
```

---

## The Core Operations

| Operation | Code | Purpose |
|---|---|---|
| **Resize** | `cv2.resize(img, (640, 480))` | Fewer pixels = faster robot |
| **Grayscale** | `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` | 3 numbers per pixel → 1 |
| **Blur** | `cv2.GaussianBlur(img, (5, 5), 0)` | Remove noise |
| **Edges** | `cv2.Canny(img, 100, 200)` | Keep only boundaries |

### Why this exact order?

It is not arbitrary. **Blur before edge detection**, always — without blurring,
tiny specks of noise register as edges and the robot sees hundreds of fake
boundaries. Each step throws away data the next step does not need:

```text
Camera → Image → OpenCV → Edges → Shapes → Object detected → Robot moves
```

A bottle becomes just its outline. That is enough to find and grip it.

---

## 🧪 6. Mini Project — Image Analyzer

The runnable project is [`image_analyzer.py`](../image_analyzer.py).

```bash
source .venv/bin/activate
python image_analyzer.py                # uses a generated sample image
python image_analyzer.py my_photo.jpg   # uses your own photo
```

It runs the full pipeline and **saves every step** into `output/` so you can
open the files and compare them:

```text
  original     800 x 600, 3 channel(s), 1,440,000 numbers
  resized      640 x 480, 3 channel(s), 921,600 numbers
  grayscale    640 x 480, 1 channel(s), 307,200 numbers
  edges        640 x 480, 1 channel(s), 307,200 numbers
```

Look at those numbers. The image went from **1.4 million** numbers to
**307 thousand** — and the shapes are still perfectly recognisable. That is the
entire point of image processing: keep the meaning, drop the cost.

---

## ⚠️ 7. Common Mistakes

- **Thinking BGR is RGB.** OpenCV loads images as **B**lue-**G**reen-**R**ed,
  not RGB. Skip the conversion and your red objects look blue. This is the
  single most common OpenCV bug.
- **Loading a huge image.** A 4000×3000 photo is 36 million numbers. Resize
  first.
- **Wrong file path.** `cv2.imread()` does not raise an error on a missing
  file — it silently returns `None`, and you crash later on a confusing line.
  Always check `if image is None`.
- **Not using a virtual environment.** Sooner or later two projects need
  different versions and you break both.
- **Edge detection without blurring first.** You will detect noise, not edges.

---

## 🎯 8. Interview Questions

**Q: What does OpenCV do?**

> OpenCV processes images and video so that computer vision and AI
> applications can be built on top of them.

<details>
<summary>Q: Why convert to grayscale before edge detection?</summary>

Edges are defined by changes in **brightness**, not colour, so colour adds
three times the data without adding useful information. Grayscale makes the
operation about 3× cheaper for an identical result. You keep colour only when
the task genuinely needs it — for example detecting a red traffic light.
</details>

<details>
<summary>Q: What is the difference between OpenCV and an AI model like YOLO?</summary>

OpenCV performs **fixed, hand-written operations** — resize, blur, find edges.
It has no idea what an object *is*. YOLO is a **trained neural network** that
recognises objects it has learned from data. In practice they work together:
OpenCV prepares the image, the model interprets it.
</details>

---

## 🚀 9. Next Topics

With OpenCV working, the path forward is:

```text
OpenCV ✅ → Shape detection → Colour tracking → Object detection (YOLO)
       → Robot camera in simulation → ROS 2 integration → Real robot
```

The next natural step is giving our **simulated robot a camera**, so instead of
processing photos from disk we process what the robot actually sees — the same
code, but live.
