# RoboticsFemme — Reel Scripts

Ready-to-film shot lists. Each one is timed, with the exact on-screen text and
what to record.

---

## 🎥 Reel 1 — "I Built My First AI Vision Robot 🤖"

**Length:** ~30 seconds · **Source:** [`yolo_camera.py`](../yolo_camera.py)

### What to record first

```bash
source .venv/bin/activate
python yolo_camera.py
```

Screen-record the window (⌘⇧5) while holding up: a **bottle**, your **phone**,
then pointing at your **laptop**. Get ~40 seconds of footage; you will cut it
down.

### Shot list

| Time | Shot | On-screen text | Voiceover |
|---|---|---|---|
| 0–3s | Your face, then cut to a plain webcam feed | **"Your laptop camera sees… nothing."** | "This is just a camera." |
| 3–7s | Same feed, now with YOLO boxes appearing | **"Until you add AI."** | "Now watch." |
| 7–13s | Hold up a bottle → box reads `bottle 0.91` | **"bottle — 91%"** | "It knows what it's looking at." |
| 13–18s | Show phone → `cell phone 0.94` | **"cell phone — 94%"** | — |
| 18–23s | Point at laptop → `laptop 0.96` | **"laptop — 96%"** | "And where it is." |
| 23–27s | Close-up of the FPS counter | **"Real time. On a MacBook Air."** | "No cloud. No GPU." |
| 27–30s | Cut to black | **"Next: the robot FOLLOWS the object."** | "Follow @RoboticsFemme" |

### Caption

```text
Day 35 of building an AI robot 🤖

My laptop camera can now recognise objects in real time —
person, bottle, phone, laptop — each with a confidence score.

This is YOLO: the model looks at the frame ONCE and finds
everything in it. That's why it's fast enough for robots.

Next: making the robot follow what it sees.

#Robotics #ComputerVision #YOLO #AI #Python #RoboticsFemme
```

### Why this hook works

It opens with a **negative** — "sees nothing" — then pays it off. A reel that
opens "today I learned about YOLO" gets scrolled past; one that shows a plain
webcam and then transforms it does not.

---

## 🎥 Reel 2 — "Why Your Robot Sees in HSV, Not RGB"

**Length:** ~25 seconds · **Source:**
[`image_processing_demo.py`](../image_processing_demo.py) — **already produces
this output**

| Time | Shot | On-screen text |
|---|---|---|
| 0–3s | The red ball image | **"Find the red ball. Easy?"** |
| 3–8s | Dim the image progressively | **"Now turn the lights down."** |
| 8–15s | The results table on screen | **"RGB: 2/5 ❌   HSV: 5/5 ✅"** |
| 15–22s | Diagram: HSV split into Hue / Saturation / Value | **"HSV separates COLOUR from BRIGHTNESS."** |
| 22–25s | — | **"That's why robots convert to HSV first."** |

Strong because it is a **measured result**, not an opinion.

---

## 🎥 Reel 3 — "My Robot Drove Under a Table 😅"

**Length:** ~30 seconds · **Source:** Lesson 10's real failure

| Time | Shot | On-screen text |
|---|---|---|
| 0–4s | Webots clip of the robot wedged under the table | **"My robot got stuck. Again."** |
| 4–10s | Side-view diagram: lidar beam passing under the tabletop | **"Its laser scans at 30cm."** |
| 10–16s | Same diagram, tabletop highlighted at 74cm | **"The tabletop is at 74cm."** |
| 16–24s | — | **"The sensor said 'clear'. It was looking UNDER the table."** |
| 24–30s | Cut to a Tesla/robot image | **"This is why real robots use camera + radar + lidar."** |

**Post your failures.** They perform better than successes, and they prove you
are actually building rather than following along.

---

## 🎥 Reel 4 — "A Map Is Useless If You're Lost"

**Length:** ~25 seconds · **Source:** [`slam_demo.py`](../slam_demo.py)

| Time | Shot | On-screen text |
|---|---|---|
| 0–4s | The clean ASCII map | **"A robot mapped this room. 100% accurate."** |
| 4–10s | The smeared map | **"Same robot. Same room. Same sensor."** |
| 10–16s | — | **"69%. The walls doubled."** |
| 16–22s | — | **"The laser was never wrong. Its POSITION was."** |
| 22–25s | — | **"That's why it's called SLAM — you must solve both at once."** |

---

## 🎥 Reel 5 — "Same Answer, 29% Less Work"

**Length:** ~20 seconds · **Source:**
[`path_planning_demo.py`](../path_planning_demo.py)

| Time | Shot | On-screen text |
|---|---|---|
| 0–4s | Dijkstra's search fanning out in a circle | **"Dijkstra checks everywhere."** |
| 4–9s | A*'s search stretching toward the goal | **"A* guesses where the goal is."** |
| 9–15s | Both paths side by side | **"Same path. 161 cells vs 114."** |
| 15–20s | One line of code highlighted | **"The difference? `+ heuristic(cell, goal)`"** |

---

## 🎥 Reel 6 — "One Phone Camera, Four AI Vision Modes"

**Length:** 35 seconds · **Status:** ✅ **already rendered** —
`video_out/robot_vision_reel_vertical.mp4` (1080×1920, silent, 5.0 MB)

**Source:** [`mobile_vision_api.py`](../mobile_vision_api.py), recorded in
[`assets/robot-vision-live-demo.mp4`](../assets/robot-vision-live-demo.mp4)

### Shot list (as cut)

| Time | Shot | On-screen text |
|---|---|---|
| 0–2s | Camera warming up, then the first detection box snaps on | **"THIS IS JUST A PHONE CAMERA"** |
| 2–4s | `id:12 person 0.83` box tracking an arm | **"UNTIL YOU ADD AI"** · *object detection* |
| 4–11s | Pink teddy and a bottle filled with pixel masks | **"IT DOESN'T DRAW A BOX"** · *"it draws the shape"* |
| 11–17s | Three tracked objects, IDs riding along with them | **"THE PERSON IS ALWAYS ID 10"** · *"same ID every time they reappear"* |
| 17–25s | Distance mode, bottle and toothbrush ranked near/far | **"AND HOW FAR AWAY IT IS"** · *"lower number = closer"* + the relative-not-metres caveat |
| 25–30s | Teddy bear held close, `23 ms` on the metric card | **"23 ms PER FRAME"** · *"no cloud. no GPU."* |
| 30–35s | Same shot, steady | **"NEXT: ON THE PHONE ITSELF"** · *"native Android · on-device"* |

The reel is exported **silent** on purpose — add trending audio in the
Instagram editor, and the first 3 seconds already work muted.

### Caption

```text
Day 43 of building an AI robot 🤖

One phone camera. Four vision modes, all running live on a MacBook Air M1:

📦 Detection — what it is, and where it is
🎨 Segmentation — the exact shape, pixel by pixel, not just a box
🔢 Multi-object tracking — every object keeps its own ID, even after it
   leaves the frame and comes back
📏 Relative distance — which object is nearer

23 ms per frame. No cloud. No GPU. No paid API.

One honest note, because I keep seeing this oversold: that distance number
is RELATIVE, not metres. A single camera physically cannot measure true
distance — for that you need stereo, a depth camera, or lidar. So the app
says "3.3 rel", not "3.3 m". Knowing what your sensor CAN'T tell you is
half of robotics.

Next: running the whole thing on the phone itself — native Android,
on-device, no server.

Full code on my GitHub 👇 (link in bio)

#Robotics #ComputerVision #YOLO #AI #Python #MachineLearning #RoboticsFemme
#WomenInSTEM #WomenInTech #DeepLearning #EdgeAI #AIEngineer #CodeNewbie
#TechReels #BuildInPublic
```

### Why this hook works

Same negative-then-payoff shape as Reel 1, but the middle now earns the
watch time: four visibly different modes in 35 seconds means there is a new
thing on screen every ~6 seconds, and the caveat about relative distance is
the kind of specific, unglamorous honesty that reads as *engineer* rather
than *content*.

### Rebuilding it

`ffmpeg` on this machine has **no `drawtext` filter** (built without
libfreetype), so the text is rendered to transparent PNGs with Pillow and
composited with `overlay`. Trim windows were chosen to keep the macOS Dock
and Launchpad out of frame — they are visible in the raw recording around
160–200s and after 210s.

---

## 🎥 Reel 7 — "How Does a Robot Build a Map?"

**Length:** ~22 seconds · **Source:** [`visual_slam.py`](../visual_slam.py)

The script downloads Mixkit clip #21589 (library corridor, 1920×1080, **free
commercial licence**, no faces) and burns the overlay in. Do not screen-record
this one — the mp4 is already the post.

```bash
source .venv/bin/activate
python visual_slam.py --linkedin --reel --gif
```

| Time | Shot | On-screen text |
|---|---|---|
| 0–2.5s | Navy title card | **"HOW DOES A ROBOT BUILD A MAP WHEN NOBODY GIVES IT ONE?"** |
| 2.5–8s | Library corridor, cyan feature trails lighting up | **"VISUAL SLAM"** · features / pose ticking |
| 8–18s | Split: camera left, growing bird's-eye map right | **"MAPPING: drawing the world"** · **"LOCALIZATION: estimating this pose"** |
| 18–22s | Navy closer | **"THE ROBOT IS SIMULTANEOUSLY LEARNING THE WORLD AND FINDING ITSELF INSIDE IT."** |

Output:

- `video_out/slam_linkedin_landscape.mp4` — **this is the LinkedIn upload**
- `video_out/slam_linkedin_landscape_vertical.mp4` — optional 9:16 cut
- `assets/visual-slam-poster.jpg` — thumbnail

### LinkedIn caption

```text
Day 44 of building an AI robot.

Nobody gave this robot a map. It built one anyway.

That is SLAM: Simultaneous Localization and Mapping. The robot estimates
where it is (localization) while it draws the room (mapping). Do one
without the other and the map smears — I showed that failure as ASCII
in an earlier lesson. This clip is the camera version.

What you are seeing:
• cyan trails = the corners visual SLAM actually tracks (not "objects")
• the right-hand panel = odometry, integrated frame by frame
• loop closure = "I have been here before" — the correction that stops drift

Clip: Mixkit #21589, free commercial licence. Overlay: OpenCV visual
odometry on a MacBook Air, no LiDAR, no GPU, no paid API.

This is the front-end of visual SLAM, not a full ORB-SLAM3 graph. Next:
the same idea on a virtual LiDAR in Webots, then ROS 2.

#Robotics #SLAM #ComputerVision #OpenCV #AI #Python #RoboticsFemme
#WomenInSTEM #AutonomousRobots #BuildInPublic
```

Stock footage is Mixkit's free licence (commercial use allowed, attribution
not required). Credit it anyway — it reads as an engineer, not as borrowed
B-roll.

---

## 📋 Production Checklist

Before posting **any** reel:

- [ ] Terminal frame contains **no API keys, tokens, or `.env` contents**
- [ ] No personal file paths visible (`/Users/yourname/...`)
- [ ] No faces of other people without their consent
- [ ] Text is readable on a phone — large, high contrast
- [ ] First 3 seconds work with **sound off** (most viewers watch muted)
- [ ] Caption states a specific result, not "learned a lot today"

### Recording a GIF for the GitHub README

```bash
# Record with Cmd+Shift+5, then:
ffmpeg -i demo.mov -vf "fps=12,scale=640:-1" -loop 0 demo.gif
```

Keep it under ~5 MB so GitHub renders it inline.
