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
