# RoboticsFemme — Content & Portfolio Strategy

> The goal: a page that makes a client think
> **"this engineer doesn't just watch tutorials — she builds robots."**

From here, every lesson produces learning **and** portfolio evidence.

---

## 📦 Three Pieces of Content Per Lesson

### 1️⃣ Instagram Reel (20–45 seconds)

Fast, visual, one idea only.

```text
Hook (3s)    "This is NOT AI."          → show the webcam feed
Build (15s)  "This is Computer Vision." → show OpenCV processing
Payoff (10s) show face detection working
Tease (5s)   "Next: the robot recognises objects."
CTA          Follow @RoboticsFemme 🤖
```

### 2️⃣ LinkedIn Post

Professional register, concrete learnings.

```text
Day 30 of my AI Robotics journey

Today I built my first OpenCV vision application.

Key learnings:
• Camera access and live video streaming
• Image preprocessing
• Why HSV beats RGB for colour detection under changing light

Next: YOLO object detection.

#Robotics #ComputerVision #OpenCV #AI
```

> **Make the "key learnings" specific.** "Learned OpenCV" says nothing.
> "Discovered OpenCV 5 removed CascadeClassifier, so pinned to 4.x" shows a
> working engineer. Specific beats polished.

### 3️⃣ GitHub

Every project needs: `README.md` · code · images · demo GIF ·
`requirements.txt`

---

## 🎬 Recording a Demo GIF (macOS)

A demo GIF in the README is the single highest-value addition to a portfolio
repo — a recruiter sees the robot working without cloning anything.

```bash
# 1. Record the screen: press Cmd + Shift + 5, choose a region, record
# 2. Convert the .mov to a GIF (ffmpeg required: brew install ffmpeg)
ffmpeg -i demo.mov -vf "fps=12,scale=640:-1" -loop 0 demo.gif
```

Then in the README:

```markdown
![Demo](demo.gif)
```

Keep GIFs under ~5 MB — GitHub will not display very large ones inline.

---

## 📹 Reel Ideas by Topic

| Topic | Ideas |
|---|---|
| **Robotics basics** | What is a robot? · Humanoid vs mobile · Industrial vs service |
| **Electronics** | Breadboard in 30s · What is a resistor? · Servo, DC and stepper motor demos |
| **Arduino** | Blink an LED · Control a servo · Read a sensor · Bluetooth robot |
| **Raspberry Pi** | Pi camera · AI on a Pi · GPIO · Smart home |
| **Jetson** | Why Jetson? · AI at the edge · Object detection · TensorRT speed test |
| **ROS 2** | What is ROS 2? · Nodes · Topics · Publisher vs subscriber · Launch files |
| **OpenCV** | Webcam in Python · Face detection · Colour detection · QR codes · OCR |
| **YOLO** | Detect person / phone / bottle / chair / laptop · Custom training |
| **Robot arm** | Pick and place · Inverse kinematics · Gripper demo |
| **AI** | LLM inside a robot · Voice robot · Vision robot · Agent robot |
| **Humanoids** | Figure AI · Tesla Optimus · Unitree G1 · Boston Dynamics Atlas |

### Content you already have footage for

These lessons produced **real, recordable output** — no new work needed:

| Reel | Source |
|---|---|
| "A robot's first steps" | [`worlds/movebot.wbt`](../worlds/movebot.wbt) |
| "Watch a robot avoid obstacles by itself" | [`worlds/movebot_avoid.wbt`](../worlds/movebot_avoid.wbt) |
| "This is what your webcam really sends" (55M numbers/sec) | [`camera_app.py`](../camera_app.py) |
| "Why robots see in HSV, not RGB" (2/5 vs 5/5) | [`image_processing_demo.py`](../image_processing_demo.py) |
| "Why a robot got stuck under a table" | Lesson 10's lidar blind spot |
| "Dijkstra vs A\*, same answer, 29% less work" | [`path_planning_demo.py`](../path_planning_demo.py) |
| "Why a map is useless if you don't know where you are" | [`slam_demo.py`](../slam_demo.py) |

> The **failures** make the best content. "My robot drove under a table because
> its laser scanned below the tabletop" is far more engaging — and more
> credible — than a demo that worked first try.

---

## 📅 Weekly Project Plan

| Week | Project |
|---|---|
| 1 | Robot camera → OpenCV → live video ✅ *(done — Lesson 30)* |
| 2 | Face detection ✅ *(done — Lesson 32)* |
| 3 | YOLO object detection |
| 4 | QR scanner robot |
| 5 | Voice-controlled robot |
| 6 | Object-following robot |

---

## 🎯 Portfolio Projects That Attract Clients

1. 🤖 AI security robot
2. 🚗 Self-driving mini car
3. 📦 Warehouse picking robot
4. ☕ Coffee serving robot
5. 🏠 Smart home assistant robot
6. 🧹 AI cleaning robot
7. 🎤 Voice-controlled robot
8. 📷 Face tracking robot
9. 📍 QR delivery robot
10. 🛒 Shopping assistant robot
11. 🦾 Robot arm pick-and-place
12. 🌾 Smart agriculture robot
13. 🏥 Hospital assistant robot
14. 🚁 AI drone vision
15. 🤝 Humanoid AI assistant

---

## 🌐 Official Documentation

Bookmark these — they outlast any tutorial:

- [Ultralytics (YOLO) Docs](https://docs.ultralytics.com/)
- [Ultralytics Quickstart](https://docs.ultralytics.com/quickstart/)
- [Ultralytics ROS Quickstart](https://docs.ultralytics.com/guides/ros-quickstart/)
- [OpenCV Docs](https://docs.opencv.org/)
- [ROS 2 Docs](https://docs.ros.org/)
- [Webots Docs](https://cyberbotics.com/doc/guide/index)
- [NVIDIA Isaac Sim Docs](https://docs.isaacsim.omniverse.nvidia.com/)

## 🎬 YouTube Channels

| Channel | Covers |
|---|---|
| NVIDIA Developer | Isaac Sim, Jetson, CUDA |
| Open Robotics | ROS 2 concepts and official demos |
| Ultralytics | YOLO tutorials and deployment |
| Boston Dynamics | Real robot demonstrations |
| Unitree Robotics | Humanoids and quadrupeds |
| The Construct | Practical ROS 2 projects |
| DroneBot Workshop | Electronics, Raspberry Pi, Arduino |
| Paul McWhorter | Beginner-friendly Python, Arduino, vision |

---

## 💼 The Client-Magnet Reel Format

```text
🎬 Hook (3s)     "Can a robot recognise a bottle?"
🎬 Demo (15s)    live detection running
🎬 Explain (10s) "YOLO detects objects in real time."
🎬 CTA (5s)      "Follow @RoboticsFemme — AI Robotics, beginner to expert."
```

---

## 🎯 The Long-Term Goal

By the end of the course, the aim is not only knowledge but evidence:

- 50+ GitHub repositories
- 100+ Instagram reels and LinkedIn posts
- 30+ complete AI robotics projects
- A professional portfolio site and a strong freelance profile
- Real hardware experience alongside simulation
- AI agent + robotics expertise

---

## ⚠️ Two Honest Notes

**1. One strong repository beats fifty weak ones.**
A target of "50+ repositories" is easy to hit badly — fifty forks and
half-finished tutorials impress nobody. This repository, with 25+ commits
across 25 lessons and working code in every one, is already more convincing
than a list of empty projects. **Depth is the differentiator.**

**2. Never post credentials or footage carelessly.**
Reels often show a terminal. Check the frame for API keys, tokens, and
`.env` contents before posting, and remember `captures/` is git-ignored for a
reason — camera footage should not reach a public repository.
