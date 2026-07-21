# Lesson 32 — Face Detection

**Module 16 — Computer Vision**

> Your robot can now see a person.

⚠️ But first, the distinction most beginners get wrong:

## Face Detection ≠ Face Recognition

| Face Detection | Face Recognition |
|---|---|
| Locates a face | Identifies **who** it is |
| *"There is a face here"* | *"This is Naeem"* |
| Easier | Much harder |

An airport camera first asks *"is there a face?"* — detection. Only then can it
ask *"whose face?"* — recognition.

---

## 🚨 Important — OpenCV Version Warning

**This lesson requires OpenCV 4.x. It will not run on OpenCV 5.**

This was discovered while testing, not assumed:

```text
OpenCV 5.0.0
>>> cv2.CascadeClassifier
AttributeError: module 'cv2' has no attribute 'CascadeClassifier'
>>> os.listdir(cv2.data.haarcascades)
['__init__.py']          # zero cascade files
```

**OpenCV 5.0 removed `CascadeClassifier` and ships no Haar cascade files.**
Install version 4:

```bash
pip install "opencv-python<5"
```

Verified working:

```text
OpenCV 4.13.0
CascadeClassifier available: True
17 cascade files shipped
frontal face cascade loads OK: True
```

> **This is the third time this course has hit the same lesson:** the newest
> version is often not the usable one. Python 3.14 had no OpenCV package;
> OpenCV 5 has no Haar cascades. Professional robotics stacks are pinned to
> specific versions for exactly this reason — and it is why `requirements.txt`
> should pin versions, not just name packages.

---

## 📖 How Haar Cascades Work

A Haar cascade is OpenCV's **classical** (non-AI) face detector. It slides a
window across the image looking for patterns of light and dark that faces
reliably have — eyes are darker than cheeks, the nose bridge is brighter than
the eye sockets.

| ✅ Advantages | ❌ Disadvantages |
|---|---|
| Fast, runs on any CPU | Sensitive to lighting |
| Simple, no training needed | Struggles with tilted or side-on faces |
| Ships with OpenCV | Far less robust than modern models |

### Modern alternatives (2026)

| Model | Use |
|---|---|
| YOLO | General object detection |
| MediaPipe Face Detection | Mobile and real-time |
| RetinaFace | Accurate face detection |
| InsightFace / FaceNet | Face **recognition** |

---

## 💻 The Code

```python
import cv2

camera = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    success, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1,
                                           minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
```

### Line by line

| Code | Why |
|---|---|
| `cvtColor(..., BGR2GRAY)` | Haar cascades work on **brightness**, not colour |
| `detectMultiScale(...)` | Finds **all** faces, at any size |
| `rectangle(...)` | Draws the bounding box |

### The two parameters that matter

| Parameter | Meaning | Raise it → |
|---|---|---|
| `scaleFactor` (1.1) | How much the image shrinks each pass | Faster, but misses faces |
| `minNeighbors` (5) | Overlapping hits needed to accept a face | Fewer false positives, more misses |

Getting **false faces** on your wallpaper? Raise `minNeighbors`. Missing real
faces? Lower it. There is no universally correct value — tuning is the work.

---

## 🔬 Practical

```bash
source .venv/bin/activate

python face_detection.py --test     # verify the cascade loads
python face_detection.py --check    # detect on one frame, report count only
python face_detection.py            # live window with green boxes
```

Verified output:

```text
  OpenCV version : 4.13.0
  Cascade file   : haarcascade_frontalface_default.xml
  Loaded         : yes
```

[`face_detection.py`](../face_detection.py) shows a live count on screen and
labels each detected face.

> **A silent failure to know about:** `CascadeClassifier` does **not** raise an
> error on a wrong path. It returns an empty classifier that detects nothing,
> forever. Always check `cascade.empty()` — the script does.

> **Privacy:** `--test` and `--check` never save, display, or transmit an
> image. `--check` reports only how many faces were found and their box sizes.
> The `captures/` folder is git-ignored.

---

## 🤖 What the Robot Does Next

Detection is only step one:

```text
Face detected → robot turns toward the person → "Hello human"
Face detected → servo motors follow the face      (face tracking)
```

| Robot | Behaviour |
|---|---|
| **Pepper** | Detects a face, turns toward the person, starts a conversation |
| **Humanoids** | Detect a person, approach, speak |
| **Smart door** | Detect + **recognise** → unlock |

Note the smart door needs **recognition**, not just detection — otherwise it
opens for anybody with a face.

---

## ⚠️ Common Mistakes

- **Confusing detection with recognition.**
- **Skipping the grayscale conversion** — the cascade expects it.
- **Assuming Haar is always the right tool.** Modern models are far more
  reliable in difficult lighting and angles.
- **Not checking `cascade.empty()`** — silent failure.
- **Running on OpenCV 5** — the API no longer exists.

---

## 🎯 Interview Questions

**Q: Difference between Haar Cascade and YOLO?**

> Haar cascade is a traditional computer vision algorithm using predefined
> features. YOLO is a deep learning model that detects faces plus thousands of
> object categories, and is generally far more robust in complex scenes.

<details>
<summary>Q: Why does the Haar cascade need a grayscale image?</summary>

It detects **contrast patterns** — regions that are lighter or darker than
their neighbours — which depend on brightness alone. Colour adds three times
the data without adding information the algorithm uses, so converting to gray
is both required by the API and faster.
</details>

---

## 🧠 Mini Challenge

Three people in the room — how many bounding boxes does `detectMultiScale()`
return?

> **3** — one per detected face.

But test the real answer: run the live window and turn your head sideways. The
count drops to 0, because this cascade is trained on **frontal** faces. That
limitation is exactly why the industry moved to learned models.

---

## 💡 2026 Industry Reality

A humanoid's perception stack:

```text
RGB camera + depth camera + microphone
      ↓
Vision AI  →  Speech AI  →  LLM  →  Robot planning  →  Robot action
```

Combining face detection, tracking, pose estimation, gesture recognition, and
voice.

---

## 🚀 Next — Lesson 33: YOLO Object Detection

The major milestone: the robot stops recognising only faces and starts
identifying **real-world objects** — person, bottle, chair, laptop, phone, cup,
dog, car.

> **Heads-up:** `ultralytics` pulls in PyTorch, which is a very large download
> (hundreds of MB). OpenCV's 55 MB stalled repeatedly on this connection before
> finally succeeding, so plan for a good network — Lesson 16
> ([`detection_demo.py`](../detection_demo.py)) already teaches boxes and
> confidence with no install, if you want to move ahead meanwhile.
