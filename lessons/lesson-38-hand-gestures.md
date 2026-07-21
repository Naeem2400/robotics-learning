# Lesson 38 — Hand Tracking & Gesture Recognition

**Module 17 — AI Vision**

> No keyboard. No mouse. You raise a hand and the robot stops.

---

## 🎯 Lesson Goal

- Hand tracking vs hand detection
- The 21 finger landmarks
- Finger counting
- Gesture recognition
- Controlling a robot with gestures

---

## 📖 Detection vs Tracking

| Hand **detection** | Hand **tracking** |
|---|---|
| Finds that a hand is present | Finds every joint of every finger |
| One box | **21 landmarks** with x, y (and z) |

Detection tells you *there is a hand*. Tracking tells you *what the hand is
doing* — and only the second one lets you read a gesture.

### The 21 landmarks

MediaPipe numbers them 0–20: the wrist, then four points per finger (base,
two joints, tip).

The ones that matter for gestures:

| Finger | Tip | Joint below |
|---|---|---|
| Thumb | 4 | 3 |
| Index | 8 | 6 |
| Middle | 12 | 10 |
| Ring | 16 | 14 |
| Little | 20 | 18 |

---

## 🧠 How a Gesture Is Actually Recognised

It is simpler than people expect. **A finger is extended when its tip is
higher than the joint below it:**

```python
finger_is_up = tip.y < pip.y      # remember: y increases DOWNWARD
```

Do that for each finger and you get five true/false values. That pattern
**is** the gesture:

| Fingers up (thumb→little) | Gesture | Count |
|---|---|---|
| `00000` | FIST | 0 |
| `01000` | ONE | 1 |
| `01100` | PEACE | 2 |
| `01110` | THREE | 3 |
| `01111` | FOUR | 4 |
| `11111` | OPEN PALM | 5 |
| `10000` | THUMBS UP | 1 |

### ⚠️ The thumb is the exception

Every tutorial glosses over this. The four fingers fold **downward**, so a
`y` comparison works. The thumb folds **sideways**, so it needs an `x`
comparison — **and the direction flips depending on which hand it is:**

```python
if hand == "Right":
    thumb_up = tip.x < pip.x
else:                       # left hand
    thumb_up = tip.x > pip.x
```

Miss this and your thumbs-up works with one hand and fails with the other,
which is a maddening bug to chase.

---

## 🔬 Practical — Run It

```bash
source .venv/bin/activate

python hand_gestures.py --test    # gesture logic, no camera needed
python hand_gestures.py           # live camera
```

[`hand_gestures.py`](../hand_gestures.py) draws the 21 landmarks, shows each
finger's state, names the gesture, and prints the robot command it maps to.

Verified output:

```text
    fist        [00000]  0 up  ->  FIST       -> STOP
    thumbs up   [10000]  1 up  ->  THUMBS UP  -> CONFIRM
    point       [01000]  1 up  ->  ONE        -> FORWARD
    peace       [01100]  2 up  ->  PEACE      -> TAKE PHOTO
    three       [01110]  3 up  ->  THREE      -> TURN LEFT
    four        [01111]  4 up  ->  FOUR       -> TURN RIGHT
    open palm   [11111]  5 up  ->  OPEN PALM  -> START
```

### Installation — two traps, both found by testing

```bash
pip install mediapipe "opencv-contrib-python<5"

mkdir -p models
curl -L -o models/hand_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

**Trap 1 — the version pin.** Plain `pip install mediapipe` pulls OpenCV 5,
which removes `CascadeClassifier` and **breaks Lesson 32's face detection**.
Verified after installing with the pin: OpenCV stayed at 4.13.0 and Lesson 32
still passes.

**Trap 2 — the API you will find online no longer exists.** MediaPipe
**0.10.35 removed `mp.solutions` entirely**:

```python
hands = mp.solutions.hands.Hands()     # AttributeError on 0.10.35
```

```text
>>> import mediapipe as mp
>>> [a for a in dir(mp) if not a.startswith('_')]
['Image', 'ImageFormat', 'tasks']
```

Almost every tutorial and video still teaches the old API. The current one is
the **Tasks API**, which loads a downloaded `.task` model:

```python
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path="models/hand_landmarker.task"),
    num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
result = detector.detect(image)
# result.hand_landmarks -> 21 NORMALISED (0-1) points per hand
# result.handedness     -> "Left" / "Right"
```

Two further differences: the Tasks API returns **normalised** coordinates
(multiply by frame width/height before drawing), and it provides **no drawing
helper** — `hand_gestures.py` draws the skeleton itself.

> **This is the fifth version conflict in this course.** It is the single most
> useful habit it can teach you: *test the library you actually have installed,
> not the one the tutorial was written against.*

> ⚠️ **The `<5` is required.** Plain `pip install mediapipe` pulls OpenCV 5,
> which removes `CascadeClassifier` and **breaks Lesson 32's face detection**.
> This is the fourth version conflict in this course — it is why
> `requirements.txt` pins versions.

### Two details in the code worth copying

**1. The image is mirrored** (`cv2.flip(frame, 1)`). Without it, moving your
hand right moves it *left* on screen and the interaction feels broken. Note
this also flips which hand MediaPipe reports, so the handedness label must be
swapped back — otherwise the thumb logic inverts.

**2. `--test` runs without MediaPipe installed.** The gesture logic is pure
Python, so the import is lazy. Good practice generally: keep your logic
separate from your I/O, and you can test it anywhere.

---

## 🤖 Gesture → Robot Command

```text
camera → hand tracking → 21 landmarks → gesture → robot command
```

| Gesture | Command | Real use |
|---|---|---|
| ✊ Fist | **STOP** | Emergency stop |
| ☝️ One | **FORWARD** | Move |
| ✌️ Peace | **TAKE PHOTO** | Capture |
| 🖐 Palm | **START** | Begin task |
| 👍 Thumb | **CONFIRM** | Accept |

The mapping is arbitrary — define your own. But note the sensible choice
above: **fist means stop**. A closed hand is the fastest, most instinctive
gesture under stress, so it should be the safety command.

---

## 🌍 Industry Applications

Contactless hospital systems · smart TVs · VR gaming · human–robot
collaboration · industrial automation · sign language research

| Robot | Gesture |
|---|---|
| Warehouse robot | 👍 → start delivery |
| Smart home | ✋ → lights off |
| Robot arm | ✌️ → pick object |
| Drone | 🖐 → take off |

---

## 🔀 Rule-Based vs AI-Based

| | How it works | Trade-off |
|---|---|---|
| **Rule-based** (this lesson) | Count extended fingers | Instant, no training data, but only recognises gestures you write rules for |
| **AI-based** | A model learns gestures from examples | Handles variation and new gestures, but needs a dataset and training |

Rule-based is the right choice here — and it is genuinely used in production
for a small fixed gesture set. **This is the same argument as Lesson 29:
choose the simplest technique that solves your problem.**

---

## ⚠️ Common Mistakes

- **Confusing detection with recognition.** Detection finds the hand;
  recognition interprets it.
- **Ignoring lighting.** Weak light collapses tracking quality.
- **Forgetting the thumb is different.** See above.
- **Not mirroring the frame** — the interaction feels backwards.
- **Reacting to every frame.** A hand passing through "peace" on its way to
  "palm" briefly reads as PEACE. Real systems require a gesture to hold for
  several frames before acting.

---

## 🎯 Interview Questions

**Q: Difference between hand tracking and gesture recognition?**

> Hand tracking detects the hand and its landmarks. Gesture recognition uses
> those landmarks to identify a gesture and turn it into a command.

<details>
<summary>Q: How would you stop a robot reacting to accidental gestures?</summary>

Require **temporal stability**: the same gesture must be detected for N
consecutive frames (say 10, about a third of a second) before it counts. That
filters out the transitions your hand passes through on the way to the gesture
you meant. Safety-critical commands often need a confirmation gesture too — the
robot should not stop because someone waved at a friend.
</details>

---

## 🧠 Mini Challenge

The robot sees 👍 — what command do you assign?

> Anything logical: *start cleaning*, *start following*, *open door*. In our
> mapping it is **CONFIRM**.

**Then extend it:** add a rule for `01001` (index + little = "rock on"). One
line in `classify()`. That is how you build a gesture vocabulary.

---

## 🎥 Reel Idea

**"Control a Robot Without Touching It! 🤖✋"** — show your hand with the 21
landmarks drawn, then cycle 👍 → *ROBOT STARTS*, ✋ → *ROBOT STOPS*. The
on-screen command changing with your fingers is the whole video.

---

## 🏆 Portfolio Project

**AI Hand Gesture Robot Controller** — live tracking, finger counting, gesture
detection, and robot command simulation. Add README, demo video, screenshots,
and installation steps.

---

## 🚀 Next — Lesson 39: OCR

The robot stops looking only at *objects* and starts **reading text** — number
plates, medicine labels, documents, signboards. Tesseract vs EasyOCR vs
PaddleOCR.
