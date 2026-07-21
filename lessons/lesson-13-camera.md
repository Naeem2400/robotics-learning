# Lesson 13 — Camera: The Robot's Eyes 👁️

**Module 7 — Computer Vision**

> **Golden rule:** A camera *takes* an image. AI *understands* it.
> These are not the same thing.

---

## Lesson Goal

After this lesson you will understand:

- How a camera works
- What a pixel is
- What resolution is
- What FPS is
- What an RGB image is
- What OpenCV is
- How a robot "sees" an image

---

## What Is a Camera?

### Technical definition

A camera is a **vision sensor** that captures light and turns it into a
digital image.

### In plain terms

A camera is like a human eye — but only halfway. A person sees *and*
understands. A robot's camera only **takes the photo**. The understanding is
done by AI.

| Human | Robot |
|---|---|
| Eyes → Brain → *"that is a bottle"* | Camera → Image → AI model → *"bottle detected"* |

---

## What Happens Inside a Camera

```text
Light  →  Lens  →  Image sensor  →  Digital image  →  Computer
```

Light bounces off an object and enters the lens. The lens focuses it onto the
image sensor. The sensor converts that light into **numbers**.

When you take a photo on your phone, the phone does not really store a picture.
It stores **millions of numbers**. AI processes those numbers.

---

## What Is a Pixel?

This is the most important concept in the lesson.

A **pixel** is the smallest single point in an image.

Think of LEGO blocks — many small blocks together make a house. An image is
made of tiny dots, and each dot is a pixel.

```text
⬜⬜⬜⬜⬜
⬜⬛⬛⬜⬜
⬜⬛⬛⬜⬜
⬜⬜⬜⬜⬜
```

Each square = 1 pixel.

---

## Resolution

Resolution tells you how many pixels an image has.

**640 × 480** means 640 columns and 480 rows:

```text
640 × 480 = 307,200 pixels
```

A 12 MP phone camera captures 12 million pixels.

### Is higher resolution always better?

**No.**

| Higher resolution | |
|---|---|
| ✅ | Better image quality |
| ❌ | Slower to process |
| ❌ | More RAM |
| ❌ | More CPU/GPU |

Robotics is always a **balance**. A robot that sees beautifully but thinks too
slowly will crash into things. Many real robots run vision at 320×240 on
purpose.

---

## FPS (Frames Per Second)

FPS is how many images the camera captures each second.

- **10 FPS** → the robot sees 10 images per second
- **30 FPS** → 30 images
- **60 FPS** → 60 images

### Why it matters

A self-driving car at **1 FPS** would be looking at the world once a second.
At 60 km/h it travels ~17 metres between glances. That is how accidents happen.

> **Connect this to Lesson 10:** our simulated robot ran its Sense → Think →
> Act loop about 30 times a second. FPS is the *sense* half of that loop. A
> slow camera means a slow-reacting robot, no matter how clever the brain is.

---

## RGB — How Colour Works

Every colour image is built from three colours: **R**ed, **G**reen, **B**lue.

```text
One pixel:
   Red   = 255
   Green = 100
   Blue  = 30
```

Those three numbers together make one colour. Three numbers per pixel.

### Grayscale

Sometimes colour is unnecessary and only brightness matters. Then the image is
black and white — **one** number per pixel instead of three.

That is **three times less data**, which makes processing much faster. This is
why many computer vision steps throw colour away first.

---

## 🔬 Practical — Prove It Yourself

You do not need OpenCV to see that an image is just numbers:

```bash
python3 pixels_demo.py
```

[`pixels_demo.py`](../pixels_demo.py) builds a 16×16 image out of raw numbers,
prints the actual pixel values, converts it to grayscale by hand, draws it as
text, and saves two real `.png` files you can open:

```text
Resolution : 16 x 16
Pixels     : 256
Numbers    : 768  (3 per pixel: red, green, blue)

  pixel at x=8   y=8   -> R=136  G=136  B=255
```

The grayscale conversion uses the standard formula:

```python
gray = 0.299 * red + 0.587 * green + 0.114 * blue
```

Green is weighted highest because the human eye is most sensitive to green,
and blue lowest. It is not a plain average — and now you know why.

---

## How an Image Reaches the AI

```text
Camera → Image → OpenCV → Python → YOLO → Result → Robot decision
```

### What is OpenCV?

OpenCV is the world's most popular computer vision library. Think of it as a
toolkit that takes an image from the camera, processes it, and hands it to an
AI model.

**OpenCV can:** open a camera, read images, process video, detect faces,
detect objects, read QR codes, resize images — and much more.

---

## Camera vs Computer Vision

| Camera | AI / Computer Vision |
|---|---|
| Captures the image | Understands the image |
| Hardware | Software / model |
| Eyes | Brain |

---

## The Professional Pipeline

This architecture is standard across the industry:

```text
Camera → OpenCV → Image processing → AI model → Decision
       → Motor controller → Robot moves
```

**Our future project:**

```text
Camera → OpenCV → YOLO → Bottle detected → Robot moves → Bottle picked
```

That is the basic workflow of warehouse and service robots.

### Real companies

| Company | Vision stack |
|---|---|
| **Tesla** | Cameras + AI vision + decision |
| **Figure AI** | RGB cameras + depth cameras + AI models |
| **Boston Dynamics** | Stereo cameras + LiDAR + AI |
| **Amazon Robotics** | Cameras + barcode vision + navigation |

Notice every one of them uses **more than one** sensor — sensor fusion from
Lesson 12.

---

## 🎯 Interview Question

**What is the difference between a camera and computer vision?**

> A camera only captures the image. Computer vision analyses and understands
> that image.

<details>
<summary>Follow-up: why convert to grayscale before processing?</summary>

Speed and simplicity. Grayscale is one number per pixel instead of three, so
there is 3× less data to move and process. Many operations — edge detection,
thresholding, shape finding — depend only on brightness, so colour adds cost
without adding information. You keep colour only when the task needs it, such
as detecting a red traffic light.
</details>

---

## ⚡ Common Mistakes

- **Assuming higher resolution is always better** — it costs processing time,
  and a slow robot is a dangerous robot.
- **Forgetting that a camera gives numbers, not meaning** — detection requires
  a model on top.
- **Ignoring lighting** — a camera is only as good as the light available. Many
  vision failures are lighting failures, not code failures.
- **Testing only on perfect images** — real camera feeds are blurry, dark, and
  tilted.

---

## 📝 Homework (observation only)

Open your phone camera today and think about:

- How is this image being formed?
- How many pixels does it contain?
- If AI were given this image, what could it identify?

This habit builds engineering thinking.

---

## 📈 Our Journey So Far

```text
Robotics foundation ✅
Programming ✅
Robot thinking ✅
Sensors ✅
Camera basics ✅
   ↓
OpenCV (next)
Computer vision
YOLO
ROS 2 integration
Simulation
Real robot
```

---

## 🚀 Next — Lesson 14

Theory ends here. **From Lesson 14 we start coding computer vision for real.**

We will install OpenCV, open our first image in Python, inspect pixel values,
resize images, convert to grayscale, and run edge detection — all on your
MacBook, **with no hardware required**.
