# Lesson 37 — Human Pose Estimation

**Module 17 — AI Vision**

> Object detection tells the robot *"a person is there."*
> Pose estimation tells it *"that person is raising their hand."*

---

## 🎯 Lesson Goal

- What pose estimation is
- Skeletons and keypoints
- MediaPipe vs YOLO Pose
- Human motion analysis
- Human–robot interaction

---

## 📖 The Problem

You tell a robot: **"raise your hand and I'll come over."** How does it know
you raised your hand?

- From your face? ❌ No
- From object detection? ❌ It only sees a box labelled "person"

It needs to see your **joints**. That is pose estimation.

### Definition

Pose estimation detects the **keypoints (joints)** of a human body in an image
or video — effectively building a **digital skeleton**.

```text
      O   ← head
      |
  O---|---O   ← shoulders, wrists
      |
     / \
    O   O     ← knees, ankles
```

⚠️ These are **not** bones. They are points the model predicts.

### The 17 COCO keypoints

```text
nose · left/right eye · left/right ear
left/right shoulder · left/right elbow · left/right wrist
left/right hip · left/right knee · left/right ankle
```

Different models use different counts — MediaPipe's body model uses 33.

---

## 🔬 Practical — Run It

```bash
source .venv/bin/activate

python pose_estimation.py --test              # gesture logic, no camera
python pose_estimation.py --image photo.jpg   # one image
python pose_estimation.py                     # live camera
```

[`pose_estimation.py`](../pose_estimation.py) uses **YOLO Pose**, which needs
**no new installation** — ultralytics is already set up from Lesson 35.

Verified on a real photo:

```text
/tmp/bus.jpg: 3 person(s)
  person 1: 16/17 keypoints visible -> standing
  person 2:  7/17 keypoints visible -> standing
  person 3: 17/17 keypoints visible -> standing
```

> **Look at person 2: only 7 of 17 keypoints.** They were partly hidden behind
> someone else. Real pose data is **incomplete** far more often than tutorials
> suggest, which is why the script drops low-confidence points instead of
> trusting all 17. A hidden wrist returns a coordinate that looks valid but is
> meaningless — acting on it is a classic bug.

---

## 🧠 Reading a Gesture From the Skeleton

Once you have joints, gestures are simple geometry:

```python
if wrist_y < shoulder_y:
    hand_is_raised = True
```

⚠️ **Image coordinates run downward.** `y = 0` is the *top* of the frame, so a
raised hand has a **smaller** y than the shoulder. Nearly everyone writes this
comparison backwards the first time.

Verified:

```text
  hand raised  -> LEFT HAND RAISED
  hand down    -> standing
  both up      -> BOTH HANDS UP
```

The script also includes a rough **fall detector**: if the shoulders and hips
end up at nearly the same height, the person is horizontal rather than upright:

```text
PERSON MAY HAVE FALLEN
```

That single check is the basis of real elderly-care and hospital monitoring
systems.

---

## 🔀 MediaPipe vs YOLO Pose

| Model | Best for |
|---|---|
| **MediaPipe** | Fast, lightweight, mobile; 33 keypoints; face + hands + body |
| **YOLO Pose** | Robotics, multi-person; one model for boxes **and** skeletons |
| OpenPose | Research, motion analysis |

### If you want MediaPipe as well

```bash
pip install mediapipe "opencv-contrib-python<5"
```

> ⚠️ **The version pin is not optional.** MediaPipe pulls in
> `opencv-contrib-python`, and by default it would install **version 5.0** —
> which removes `CascadeClassifier` and would **break Lesson 32's face
> detection**. Constraining it to `<5` installs 4.13 instead, matching the rest
> of this project.
>
> This is the fourth time this course has hit a version conflict. Pinning
> versions is not bureaucracy; it is what keeps a robotics stack working.

```python
import mediapipe as mp

pose = mp.solutions.pose.Pose()
result = pose.process(rgb_frame)
mp.solutions.drawing_utils.draw_landmarks(
    frame, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
```

---

## 🌍 Real Applications

| System | Uses pose to |
|---|---|
| **Fitness robot** | Count squats, check form |
| **Yoga assistant** | Compare posture to a reference |
| **Hospital robot** | Detect that a patient has fallen |
| **Factory robot** | Track worker position, avoid collisions |
| **Humanoids (Figure AI, Optimus)** | Move safely around people |

```text
RGB camera → pose estimation → gesture recognition → robot planning → motors
```

---

## ⚠️ Common Mistakes

- **Confusing pose estimation with face detection.**
- **Thinking keypoints are bones.** They are predictions, and they are noisy.
- **Assuming one person only.** Modern models handle many.
- **Trusting every keypoint.** Check confidence — occluded joints return
  garbage.
- **Getting the y-axis backwards.** Up means *smaller* y.

---

## 🎯 Interview Questions

**Q: Difference between pose estimation and object detection?**

> Object detection gives an object's class and location. Pose estimation
> detects the joints and posture of a human body.

<details>
<summary>Q: How would you detect that someone has fallen?</summary>

Compare joint geometry rather than looking for a "falling" class. An upright
person has a clear vertical gap between shoulders and hips; a horizontal person
does not. Comparing that gap to shoulder width gives a scale-independent test —
it works whether the person is near or far from the camera. Production systems
add a time element too, since a *sudden* transition to horizontal is far more
suspicious than someone lying down slowly.
</details>

---

## 🧠 Mini Challenge

The robot sees 🙋 — what does it conclude?

> The user raised a hand. That can trigger a greeting, wake the robot, or start
> command mode.

**Then try it:** run the live camera and raise one hand, then both. The label
changes from `standing` → `LEFT HAND RAISED` → `BOTH HANDS UP`. Now lower your
hand slowly and watch where the threshold sits — that boundary is the gesture.

---

## 🎥 Reel Idea

**"How Does a Robot Understand Human Movement?"** — stand in frame, raise your
hand, and let the skeleton overlay plus the changing label tell the story. The
`BOTH HANDS UP` label appearing on cue is the payoff shot.

---

## 🏆 Portfolio Project

**AI Human Pose Detection System** — live webcam demo, screenshots, README,
install steps, short demo video. The fall-detection angle makes it a stronger
portfolio piece than a plain skeleton viewer, because it solves a **real
problem** a client would pay for.

---

## 🚀 Next — Lesson 38: Hand Tracking & Gesture Recognition

Finger tracking, finger counting, thumbs up, peace sign, fist — controlling a
robot with nothing but hand gestures. The foundation of touchless interfaces,
smart homes, AR/VR, and service robotics.
