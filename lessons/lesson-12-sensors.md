# Lesson 12 — Sensors: The Robot's Eyes, Ears, and Skin

**Module 6 — Sensors**

> **Golden rule:** Without sensors, a robot is just a machine. With sensors,
> it becomes aware of the world.

---

## Lesson Objectives

After this lesson you will understand:

- What a sensor is
- Why a robot cannot work without sensors
- How many types of sensors exist
- Which sensors real robots use
- Which sensors we will use in simulation

---

## What Is a Sensor?

### Technical definition

A **sensor** is a device that detects or measures information from the
environment and sends that information to the robot's controller.

### In plain terms

A robot cannot see anything by itself. The sensor collects the information and
tells it:

- There is a wall ahead
- A person is standing there
- The room is warm
- The battery is low
- The robot is facing this direction

---

## Human vs Robot

| Human | Robot |
|---|---|
| Eyes — see | **Camera** |
| Ears — hear | **Microphone** |
| Skin — feel | **Touch sensor** |
| Nose — smell | **Gas sensor** |
| Tongue — taste | **Chemical sensor** (special robots) |

A robot also senses the world — just through electronics instead of biology.

---

## Robot Architecture

```text
Environment
     ↓
  Sensors
     ↓
Robot Brain
     ↓
 Decision
     ↓
  Motors
     ↓
 Movement
```

**Remember this flow.** It is the same Sense → Think → Act loop from Lesson 10,
drawn with the sensor at the top.

---

## The Five Sensor Categories

```text
Sensors
│
├── Vision
├── Distance
├── Motion
├── Position
└── Environmental
```

### 1. Vision sensors 👁️

RGB camera, depth camera, stereo camera. They let the robot see a human, a
bottle, a chair, a car, a traffic light.

*Real use:* a Tesla reads the road with cameras; a warehouse robot reads
barcodes; a robot arm identifies the object it is about to grip.

### 2. Distance sensors 📏

Ultrasonic, LiDAR, infrared. They answer one question: **how far away is that?**

```text
Robot ---- 30 cm ---- Wall
```

*This is the sensor our simulation robot already uses.*

### 3. Motion sensors 🧭

IMU, gyroscope, accelerometer. They answer: **how much did I move or rotate?**

*Real use:* a drone cannot stay level without an IMU.

### 4. Position sensors 📍

GPS (outdoors), wheel encoders, indoor localisation. They answer: **where am I?**

*Real use:* a delivery robot locating itself on a map.

### 5. Environmental sensors 🌡️

Temperature, humidity, gas, air quality, light.

*Real use:* a farming robot checks soil moisture and starts irrigation
automatically.

---

## What Sensor Data Actually Looks Like

A sensor sends **numbers**, nothing more:

```text
Temperature = 29 °C
Distance    = 15 cm
Battery     = 78 %
Light       = 320 lux
```

The robot's brain gives those numbers meaning:

```python
if distance < 20:
    stop()
```

That is the whole job: **numbers in, decision out.**

---

## ⭐ Sensor Fusion (very important)

### Definition

Combining data from two or more sensors to make a better decision.

### Why it is necessary

Imagine you rely only on your eyes, and the lights go out. You immediately
start using your ears and your hands instead. More than one sense. Robots do
exactly the same.

```text
Camera        → "that is a bottle"
LiDAR         → "it is 60 cm away"
Depth camera  → "it is 22 cm tall"
        ↓
AI: bottle located, ready to grip
```

A self-driving car fuses camera + LiDAR + radar + GPS + IMU. **One sensor is
never enough.**

> **You have already seen why.** In Lesson 10 our robot drove under a table
> because its single 2D lidar scanned *below* the tabletop and reported "clear".
> A camera or a second sensor plane would have caught it. That failure is
> exactly the argument for sensor fusion.

---

## Which Sensors We Will Learn

| Sensor | Learn in simulation | Real hardware later |
|---|---|---|
| Camera | ✅ | ✅ |
| LiDAR | ✅ | ✅ |
| Ultrasonic | ✅ | ✅ |
| IMU | ✅ | ✅ |
| GPS | ✅ | ✅ |
| Wheel encoder | ✅ | ✅ |
| Microphone | ✅ | ✅ |
| Depth camera | ✅ | ✅ |

---

## 2026 Industry Trend

Modern robots do not just *read* sensors — they use AI to understand what the
readings **mean**:

```text
Camera image → AI: "that is a worker"
LiDAR        → 2.1 m away
Robot        → "maintain a safe distance"
```

**Sensor + AI = an intelligent robot.**

---

## 🔬 Practical — See Real Sensor Data

Reading about sensors is abstract. Let us look at actual numbers.

```bash
open -a Webots worlds/sensor_lab.wbt    # then press Run
```

The robot slowly turns in place while
[`controllers/sensor_explorer/sensor_explorer.py`](../controllers/sensor_explorer/sensor_explorer.py)
does two things:

1. **Lists every sensor the robot has** — so you can see its real hardware.
2. **Prints live distance readings** in four directions, with a simple bar
   chart, so you can watch the numbers change as it rotates:

```text
FRONT |########             | 1.42 m
LEFT  |###                  | 0.51 m
RIGHT |###############      | 2.60 m
BACK  |####################| no echo
```

Watch what happens as a wall comes into view — that stream of numbers is
*everything* the robot knows about the world.

---

## 🎯 Interview Question

**What is the main job of a sensor?**

> A sensor collects information from the environment and sends it to the
> robot's controller or AI system, so the robot can make a decision.

<details>
<summary>A harder follow-up: what is sensor fusion, and why does it matter?</summary>

Sensor fusion combines data from multiple sensors so their strengths cover each
other's weaknesses. A camera sees colour and texture but judges distance poorly;
a lidar measures distance precisely but sees no colour; radar works in fog where
both struggle. Fusing them gives a more reliable picture than any one alone —
and removes the single points of failure that cause accidents.
</details>

---

## 📝 Homework (thinking only)

You are building a **hospital service robot** that delivers medicine to
patients. **Which sensors would you use, and why?**

Consider: camera? LiDAR? microphone? IMU? touch sensor?

<details>
<summary>Some things to think about</summary>

There is no single right answer, but a strong one explains *why* each sensor
earns its place — and what fails without it:

- **LiDAR** — navigate corridors and avoid people. Without it, it cannot move
  safely at all.
- **Camera** — read room numbers, recognise staff, identify the right patient.
- **Microphone** — respond when a patient speaks to it.
- **IMU + encoders** — know its own position between map updates.
- **Touch/bumper** — a last-resort safety stop if everything else misses
  something. In a hospital, that redundancy is not optional.

Notice this is **sensor fusion** in practice: no single sensor makes this robot
work.
</details>

---

## 🚀 Next — Lesson 13

**Camera — the robot's eyes.** How an image is captured, what a pixel is,
resolution, FPS, RGB vs grayscale, what OpenCV is, and how AI "sees" an image.
Then we process our first image with Python and OpenCV — **no hardware
required**.
