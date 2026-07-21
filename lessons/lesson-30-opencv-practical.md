# Lesson 30 — OpenCV Practical (Your First AI Vision Program)

**Module 16 — Computer Vision**

> No more reading. Real code, running on your camera.

---

## 🎯 Goal

- Install OpenCV ✅
- Access the camera ✅
- See live video
- Save a photo
- Record a video

---

## 📁 Step 1 — Project Structure

```text
Project_01_OpenCV_Camera/
├── main.py
├── requirements.txt
├── README.md
└── captures/          photos and video (git-ignored)
```

Scaffold one instantly with the Lesson 23 script:

```bash
bash new_project.sh Project_01_OpenCV_Camera
```

---

## 🐍 Step 2 — Environment and Install

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install opencv-python
```

Verify:

```bash
python -c "import cv2; print(cv2.__version__)"
```

### ✅ Verified on this machine

```text
OpenCV 5.0.0
```

> **Why `python3.13` and not `python3`?** The system Python here is 3.14, and
> OpenCV publishes no prebuilt package for it — pip would try to compile from
> source and fail. This is a real robotics skill: the newest version is often
> not the usable one.

---

## 📷 Step 3 — Open the Camera

```python
import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    if not success:
        break

    cv2.imshow("Robot Camera", frame)

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
```

| Line | Meaning |
|---|---|
| `VideoCapture(0)` | The first camera on the machine |
| `camera.read()` | Grab one frame |
| `cv2.imshow()` | Show it on screen |
| `cv2.waitKey(1)` | Listen for a keypress for 1 ms |
| `camera.release()` | **Hand the camera back** — skip this and it stays locked |

---

## 🔬 Step 4 — Run the Live Experiment

```bash
source .venv/bin/activate
python camera_app.py --test      # check the camera, no window
python camera_app.py             # the live window
```

### ✅ Actual output from this MacBook

```text
Camera 0 opened: 1280 x 720 pixels
  Frame size : 1280 x 720
  Channels   : 3 (blue, green, red - OpenCV uses BGR)
  Data type  : uint8
  Numbers    : 2,764,800 per frame
  At 20 fps that is 55 million numbers per second.
```

**Stop and look at that last number.** Your webcam produces **55 million
numbers every second**. Lesson 15 said an image is just numbers; this is the
scale of it. Everything in computer vision — resizing, grayscale, edge
detection — exists to cut that firehose down to something a robot can act on
in time.

---

## 🧪 Step 5 — The Mini Challenge, Solved

The challenge asked for keyboard control. It is implemented in
[`camera_app.py`](../camera_app.py):

| Key | Action |
|---|---|
| **C** | Capture a photo |
| **R** | Start recording |
| **T** | Stop recording |
| **Q** | Quit |

The current state is drawn onto the video itself — green `live`, red
`RECORDING` — so you can always see what the program is doing.

> **Privacy note:** captures go into `captures/`, which is **git-ignored**.
> Never commit camera footage to a public repository. This matters more than
> it sounds — people routinely push webcam frames and screen recordings to
> GitHub without thinking.

---

## 🐞 Step 6 — Debugging

### The camera will not open

**System Settings → Privacy & Security → Camera → allow your terminal or
VS Code.**

⚠️ **The failure mode is nasty:** if permission is denied, OpenCV does **not**
raise an error. `isOpened()` returns `True` and `read()` returns empty frames
forever. That is why `camera_app.py` tests a real frame instead of trusting
`isOpened()`.

### Black screen

Another app holds the camera — quit Zoom, Teams, or FaceTime.

### "Can't open camera"

Try a different index — `cv2.VideoCapture(1)` or `(2)`. The script tries 0, 1
and 2 automatically.

### The video file is created but empty

The size given to `VideoWriter` must **exactly match** the frame size. A
mismatch produces a valid but empty file, with no error.

---

## 🏗️ Architecture

```text
Camera → Frame → OpenCV → Python → Screen
```

The real robot version:

```text
Camera → OpenCV → YOLO → ROS 2 → Motor controller → Robot
```

| Robot | Pipeline |
|---|---|
| **Warehouse** | Camera → OpenCV → YOLO → box found → pick |
| **Tesla** | Camera → frames → AI → road detection → steering |
| **Boston Dynamics** | Stereo camera → depth → OpenCV → navigation |

---

## 💡 Industry Tip — Never One Big File

```text
Project/
├── camera.py       camera handling
├── utils.py        helpers
├── config.py       settings, no magic numbers in code
├── main.py         entry point
├── tests/
├── README.md
└── requirements.txt
```

---

## 🎯 Interview Question

**Difference between `cv2.imread()` and `cv2.VideoCapture()`?**

> `imread()` loads a single image from disk. `VideoCapture()` opens a camera
> or video file and returns frames one at a time.

<details>
<summary>Follow-up: why must you call camera.release()?</summary>

The camera is an exclusive hardware resource. Until it is released, the
operating system keeps it locked to your process — so your next run, or Zoom,
will find a black screen. Crashing out of a script without releasing is the
usual reason a camera "stops working" until you reboot.
</details>

---

## 💡 2026 Industry Trend

Modern vision systems combine OpenCV with the latest YOLO release, Vision
Transformers (ViT), SAM2 (Segment Anything), depth estimation models, and
multimodal vision-language models.

**OpenCV remains the foundation** — the layer that gets pixels in and prepares
them.

---

## 🚀 Next — Lesson 31: Image Processing

Resize, crop, rotate, blur, edge detection, drawing shapes and text — then on
to face detection and YOLO object detection.

> **A head start:** [`image_analyzer.py`](../image_analyzer.py) from Lesson 14
> already runs the resize → grayscale → blur → edge pipeline and saves each
> stage to `output/`. Now that OpenCV is installed it has been verified
> working — run it and compare the five images.
