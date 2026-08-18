# Lesson 1 — What Is a Robot?

**Module 1 — Robotics Introduction**

> **Golden rule:** A machine repeats. A robot *senses, decides, and acts*.
> Everything in this bootcamp is built on that one sentence.

---

## Lesson Objectives

After this lesson you will understand:

- What actually makes something a robot
- The Sense → Think → Act loop that every robot runs
- The difference between automation, robotics, and AI
- The main categories of robots and where they are used
- The five levels of autonomy, and where today's robots really sit

---

## The Definition

### Technical definition

A **robot** is a programmable machine that can **sense** its environment,
**process** that information, and **act** on the physical world.

### The test

Three questions. A robot answers **yes** to all three:

| Question | Answered by |
|---|---|
| Can it perceive the world? | Sensors |
| Can it decide what to do? | Controller / AI |
| Can it change the physical world? | Actuators |

A washing machine fails the first question — it follows a timer, it does not
perceive. A weather app fails the third — it processes information but moves
nothing. A robot vacuum answers yes three times.

---

## The Loop That Defines Robotics

```text
        ┌──────────────────────────┐
        │                          │
        ▼                          │
     SENSE                         │
   (camera, lidar)                 │
        │                          │
        ▼                          │
     THINK                    feedback
   (code, AI)                      │
        │                          │
        ▼                          │
      ACT                          │
   (motors)                        │
        │                          │
        └──────────────────────────┘
```

Every robot ever built runs this loop — a $30 line follower and a Waymo
alike. The difference between them is **not** the loop. It is:

- how good the sensing is,
- how smart the thinking is,
- how fast the loop runs.

A self-driving car runs this loop roughly 30–100 times per second. If it ran
once per second, it would be lethal.

---

## Automation vs Robotics vs AI

These three words get used interchangeably, and they should not be.

| | Perceives? | Decides? | Acts physically? | Example |
|---|---|---|---|---|
| **Automation** | ❌ | Fixed rules | ✅ | Factory conveyor, washing machine |
| **Robotics** | ✅ | ✅ | ✅ | Robot vacuum, warehouse AMR |
| **AI** | ✅ (data) | ✅ | ❌ | ChatGPT, a fraud detector |
| **AI Robotics** | ✅ | ✅ *learned* | ✅ | Tesla FSD, a humanoid picking laundry |

**Automation** repeats a fixed sequence. It does not care that the world
changed.

**Robotics** closes the loop with sensors, so the machine adapts.

**AI** is the thinking part — and on its own, it has no body.

**AI Robotics** — this bootcamp — is what happens when you give the AI a body.
That is the whole field in one line, and it is why the industry calls it
**embodied AI**.

---

## Categories of Robots

```text
Robots
│
├── Industrial      — robot arms, welding, assembly
├── Mobile          — AMRs, delivery robots, rovers
├── Service         — vacuum, hospital, hotel, agriculture
├── Humanoid        — Figure, Optimus, Unitree
├── Aerial / Marine — drones, underwater ROVs
└── Medical         — surgical robots (da Vinci)
```

Note what changes between categories: **the body and the sensors**. The Sense →
Think → Act loop does not change. This is why the skills transfer — learn to
program a simulated two-wheel robot properly and you have learned the pattern
that a surgical robot uses.

---

## The Five Levels of Autonomy

Borrowed from the automotive standard, but it applies to any robot:

| Level | Name | Who is in control | Example |
|---|---|---|---|
| 0 | Manual | Human, fully | RC car |
| 1 | Assisted | Human, machine helps | Cruise control |
| 2 | Partial | Machine acts, human watches | Tesla Autopilot |
| 3 | Conditional | Machine drives, human is backup | Limited highway systems |
| 4 | High | No human, inside a defined area | Waymo in mapped cities |
| 5 | Full | No human, anywhere | **Does not exist yet** |

> **Be honest about this in interviews.** No shipping robot is Level 5. Anyone
> claiming a general-purpose fully autonomous robot in 2026 is selling
> something. Most real deployments are Level 4 *inside a well-mapped
> environment*, which is a genuinely hard and valuable thing to build.

---

## Why Robotics Is Hard (Moravec's Paradox)

Here is the thing that surprises every newcomer:

```text
Chess grandmaster level     →  solved in 1997
Reading a legal contract    →  solved
Folding a towel reliably    →  still hard in 2026
```

**Moravec's paradox:** the things humans find hard (chess, maths, exams) are
easy for computers, and the things a two-year-old does effortlessly (grabbing a
cup, walking on gravel, recognising a friend) are extraordinarily hard for
machines.

Why? Evolution spent hundreds of millions of years on perception and movement,
and only a few thousand on algebra. The hard part of robotics is not the
thinking. **It is the sensing and the acting.**

That is exactly why this bootcamp spends most of its time on vision and
control, not on clever algorithms.

---

## 2026 Industry Trend

Three shifts define robotics right now:

1. **Foundation models moved into the body.** Vision-Language-Action (VLA)
   models take a camera image and an instruction in English and output motor
   commands directly, instead of a human hand-coding every behaviour.
2. **Humanoids got funded.** Figure, Tesla Optimus, Unitree and others are
   betting that a human-shaped robot can use human tools and human spaces
   without redesigning the factory.
3. **Simulation-first is standard.** Companies train in Isaac Sim, Webots or
   MuJoCo and transfer to hardware. Learning in simulation is not the cheap
   version of robotics — **it is how the industry works.**

---

## 🔬 Practical — Your First Sense → Think → Act Loop

No hardware, no simulator. Just the loop, in plain Python:

```bash
python3 robot.py
```

Look at the output of *Project 3: Obstacle check*:

```text
--- Project 3: Obstacle check ---
Robot stop
```

Now open [`robot.py`](../robot.py) and find the code that produced it. It is
this shape:

```python
distance = 15                 # SENSE  — centimetres, from the ultrasonic sensor
if distance < 20:             # THINK  — the decision
    print("Robot stop")       # ACT    — a print here; a motor command on hardware
else:
    print("Move")
```

That is a complete robot control loop. Everything else in this bootcamp —
lidar, YOLO, SLAM, path planning — makes each of those three lines smarter. The
shape never changes.

---

## 🎯 Interview Question

**What is the difference between automation and robotics?**

> Automation executes a fixed, pre-programmed sequence regardless of what is
> happening around it. Robotics closes the loop with sensors: the machine
> perceives its environment, decides based on what it perceived, and acts —
> so it adapts when conditions change.

<details>
<summary>A harder follow-up: is a CNC machine a robot?</summary>

Usually **no**, and the reason is instructive. A CNC mill acts on the physical
world with great precision, and it is programmable — but it follows a fixed
toolpath and does not perceive the workpiece. Change the material or misalign
the stock and it cuts confidently into empty air.

Add a probe or a vision system that measures the actual part and adjusts the
path, and it starts to qualify. The dividing line is **perception feeding
back into the decision**, not precision, cost, or how impressive the machine
looks.
</details>

---

## 📝 Homework (thinking only)

Pick three machines in the room you are sitting in. For each one, answer:

1. Does it sense? What does it sense with?
2. Does it decide, or does it just follow a fixed sequence?
3. Does it act on the physical world?

Then decide: automation, robot, or neither?

<details>
<summary>Worked example — a modern air conditioner</summary>

- **Senses?** Yes — a temperature sensor, and often a motion sensor.
- **Decides?** Yes, in a limited way: it compares the measured temperature to
  the target and switches the compressor accordingly.
- **Acts physically?** Yes — it moves air and changes the room temperature.

So it passes all three tests, and by a strict reading it is a very simple
robot. Most engineers would call it a **closed-loop control system** instead,
and reserve "robot" for machines with richer perception and more than one
degree of freedom.

The useful takeaway is that the boundary is a spectrum, not a wall. What
matters is the loop.
</details>

---

## 🚀 Next — Lesson 2

**Robot components.** We open the robot up: the chassis, the actuators, the
sensors, the controller, and the power system — what each part does, and which
one is most likely to be the reason your robot does not work.
