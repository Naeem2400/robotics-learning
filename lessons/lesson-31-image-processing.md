# Lesson 31 — Image Processing Fundamentals

**Module 16 — Computer Vision**

> Get this lesson right and OpenCV, YOLO, face detection, and OCR all become
> much easier. Image manipulation is the first step of every vision pipeline.

---

## 🎯 Lesson Goal

Resize · crop · rotate · flip · draw shapes · add text · blur · edge detection
· colour spaces

---

## 📖 The Idea — Preprocessing

A robot needs to detect a bottle. The camera's raw image is **not** handed
straight to the AI:

```text
Camera → Resize → Remove noise → Improve contrast → AI model → Prediction
```

This is **image preprocessing**, and it exists because raw camera data is far
too large and too messy. Recall from Lesson 30: your webcam produces
**55 million numbers per second**.

---

## 🔬 Practical — Run Every Operation

```bash
source .venv/bin/activate
python image_processing_demo.py
```

[`image_processing_demo.py`](../image_processing_demo.py) runs each operation
and saves the result to `output_processing/` so you can compare them:

```text
  file                 size  ch   note
  01_original       480x360   3   the starting image
  02_resized        240x180   3   half size, quarter the pixels
  03_cropped        140x140   3   just the ball
  04_rotated        360x480   3   for an upside-down camera mount
  05_flipped        480x360   3   mirror image
  06_gray           480x360   1   3 channels -> 1, three times less data
  07_blurred        480x360   1   smooths noise before edge detection
  08_edges          480x360   1   only the outlines remain
  09_annotated      480x360   3   a bounding box, drawn the YOLO way
```

> **Notice `02_resized`:** halving the width and height gives **a quarter** of
> the pixels, not half. Image cost scales with *area*. This is why resizing is
> the single most effective speed optimisation in vision.

---

## 🛠️ The Operations

### Resize

```python
small = cv2.resize(image, (640, 480))
```

A phone camera gives 4032×3024. YOLO wants 640×640. Resizing is mandatory.

### Crop — just array slicing

```python
face = image[100:400, 200:500]
```

⚠️ **Rows first:** `image[y1:y2, x1:x2]`. Everyone writes it backwards once.

### Rotate and flip

```python
cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)   # upside-down camera mount
mirror = cv2.flip(image, 1)
```

### Blur

```python
blur = cv2.GaussianBlur(image, (5, 5), 0)
```

Removes noise — dust on a factory camera, sensor grain in low light. **Blur
before edge detection**, or you detect the noise instead of the object.

⚠️ But do **not** blur reflexively. Blurring destroys fine detail; if you are
reading small text or a barcode it will make things worse.

### Edge detection

```python
edges = cv2.Canny(image, 100, 200)
```

Only outlines remain — shape without colour.

### Drawing — exactly how YOLO renders results

```python
cv2.rectangle(image, (100, 100), (300, 300), (0, 255, 0), 2)
cv2.circle(image, (200, 200), 50, (255, 0, 0), 3)
cv2.line(image, (0, 0), (400, 400), (0, 0, 255), 2)
cv2.putText(image, "Robot", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
```

⚠️ **Colours are (Blue, Green, Red)** — so `(0, 255, 0)` is green and
`(0, 0, 255)` is red. Every OpenCV beginner gets this backwards.

The demo's `09_annotated.png` draws a green box labelled `ball 0.96` — the
exact output format of an object detector.

---

## 🎨 Colour Spaces — and the Mini Challenge, Tested

| Space | Meaning |
|---|---|
| **BGR** | Blue, Green, Red — OpenCV's default |
| **Gray** | Brightness only, 1 channel |
| **HSV** | **H**ue (which colour), **S**aturation (how vivid), **V**alue (how bright) |

```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
```

### The challenge

*To detect a red ball, is BGR or HSV better?* The demo photographs the same
ball at five brightness levels and tests both:

```text
  lighting         BGR finds   HSV finds
  --------------------------------------
  very bright       11289 ok    11289 ok
  normal            11289 ok    11289 ok
  dim                   0 XX    11289 ok
  dark                  0 XX    11289 ok
  very dark             0 XX    11289 ok
  --------------------------------------
  score                 2/5        5/5
```

### Why HSV wins

**BGR mixes colour and brightness together.** Dim the light and the R value
falls, so a "red" threshold stops matching — even though the object is
obviously still red.

**HSV separates them.** Hue says *what colour it is*; Value says *how bright*.
You can ask for "red hue, any reasonable brightness" and the detection survives
the lighting change.

> **This partly answers Lesson 29.** There, a colour rule failed 4 out of 5
> tests. HSV fixes the **lighting** failures — but it still cannot tell a red
> apple from a red ball. Better colour spaces solve one problem; only a trained
> model solves the other.

---

## ⚠️ Common Mistakes

- **Treating BGR as RGB.** OpenCV is BGR everywhere.
- **Feeding a full-resolution image to a model.** Resize first.
- **Blurring by default.** It is not always appropriate.
- **Slicing `image[x, y]`** instead of `image[y, x]`.
- **Thresholding colour in BGR** when lighting varies — use HSV.

---

## 🎯 Interview Questions

**Q: Why use grayscale?**

> When colour carries no useful information and speed matters. Grayscale has
> one channel instead of three, so there is three times less data to process.

<details>
<summary>Q: Why is red awkward to threshold in HSV?</summary>

Hue is a circle from 0 to 180 in OpenCV, and red sits at **both ends** — near
0 and near 180. So detecting red needs **two** ranges combined, while blue or
green need only one. The demo does exactly this; it is a classic source of "my
red detection only half works."
</details>

---

## 🏗️ Industry Architecture

```text
Camera → OpenCV → Resize → Colour conversion → Noise reduction
   → AI model (YOLO / OCR / face detection) → Prediction
```

Modern pipelines also use Albumentations (augmentation), NVIDIA CV-CUDA (GPU
processing), and PyTorch Vision transforms — but the concepts are identical:
**prepare the image for the model.**

---

## 🧠 Mentor Tip

Do not just copy code. After every function, ask:

1. **What is the input?**
2. **What is the output?**
3. **What decision will the robot make with that output?**

That habit is what turns a tutorial follower into an engineer.

---

## 🚀 Next — Lesson 32: Face Detection

Haar cascades, bounding boxes, multiple faces, live camera detection, and
performance optimisation — then on to **YOLO object detection**, where the
robot starts recognising real-world objects.
