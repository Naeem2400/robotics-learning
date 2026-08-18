# Lesson 2 — Robot Components

**Module 2 — Robot Components**

> **Golden rule:** Every robot is five subsystems. If a robot is not working,
> the fault is in one of the five — and it is usually power.

---

## Lesson Objectives

After this lesson you will understand:

- The five subsystems every robot has
- What actuators are, and how to choose between them
- Degrees of freedom, and why the number matters
- Why gearing exists and what it costs you
- How the parts talk to each other

---

## The Five Subsystems

```text
                ┌─────────────┐
                │   POWER     │  battery, regulators
                └──────┬──────┘
                       │ feeds everything
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 ┌─────────┐    ┌────────────┐    ┌──────────┐
 │ SENSORS │───▶│ CONTROLLER │───▶│ ACTUATORS│
 └─────────┘    │  (brain)   │    └────┬─────┘
      ▲         └────────────┘         │
      │                                ▼
      │                         ┌────────────┐
      └─────────────────────────│ STRUCTURE  │
              the world          │ (body)     │
                                └────────────┘
```

| Subsystem | Job | Human equivalent |
|---|---|---|
| **Structure** | Holds everything, takes the loads | Skeleton |
| **Actuators** | Convert energy into motion | Muscles |
| **Sensors** | Measure the world and the robot itself | Senses |
| **Controller** | Decide what to do | Brain |
| **Power** | Supply energy to all of it | Metabolism |

Memorise this list. When a robot misbehaves, the debugging question is always
*"which of the five?"* — and beginners almost always suspect the controller
first, when the answer is usually power or a sensor.

---

## 1. Structure — the Body

The chassis sets the robot's **shape, mass, and stiffness**, and those three
decide what the rest of the system has to cope with.

Common mobile robot layouts:

| Drive type | Wheels | Can it turn in place? | Used by |
|---|---|---|---|
| **Differential** | 2 driven + caster | ✅ | Robot vacuums, TurtleBot, our MoveBot |
| **Ackermann** | Car steering | ❌ | Self-driving cars |
| **Omni / Mecanum** | 3–4 special wheels | ✅ + sideways | Warehouse robots |
| **Tracked** | Tracks | ✅ | Rough terrain, rescue |
| **Legged** | 2–4 legs | ✅ | Spot, humanoids |

**Differential drive** is the one you will program first, and it is worth
knowing why it dominates teaching: two motors, no steering mechanism, and it can
spin on the spot. Drive one wheel forward and the other backward and the robot
rotates around its own centre.

---

## 2. Actuators — the Muscles

An **actuator** converts electrical energy into physical motion. Choosing the
right one is a real engineering decision:

| Actuator | Controls | Feedback? | Typical use |
|---|---|---|---|
| **DC motor** | Speed | ❌ (add an encoder) | Wheels, fans |
| **Servo motor** | Angle (0–180°) | ✅ built in | Robot arm joints, grippers, pan-tilt |
| **Stepper motor** | Exact steps | ❌ but precise | 3D printers, CNC |
| **BLDC motor** | Speed, high power | ✅ with driver | Drones, e-bikes, humanoid joints |
| **Linear actuator** | Push/pull distance | Varies | Lifts, presses |

The distinction that matters most:

```text
DC motor    →  "spin at this speed"     →  you do not know where it ended up
Servo       →  "go to 90 degrees"       →  it holds that angle by itself
Stepper     →  "move 200 steps"         →  precise, but it can silently skip
```

A servo is a DC motor **plus** a gearbox, a position sensor, and a small control
loop in one package. You are paying for the feedback loop — which is exactly why
it can hold a position against a load and a bare DC motor cannot.

---

## 3. Degrees of Freedom

**Degrees of freedom (DOF)** = the number of independent movements a robot can
make.

```text
Differential drive robot   →  2 DOF   (forward/back, rotate)
SCARA arm                  →  4 DOF
Industrial arm (UR5, ABB)  →  6 DOF   (position + orientation, fully)
Human arm                  →  7 DOF   (6 + a redundant elbow rotation)
```

**Why 6 is the magic number:** to place an object anywhere in space at any
angle, you need 3 DOF for position (x, y, z) and 3 for orientation (roll, pitch,
yaw). Six gets you every reachable pose. Fewer means some poses are impossible.

**Why 7 is better:** the extra DOF is *redundant* — the arm can reach the same
pose in many different configurations, so it can work around an obstacle or a
joint limit. Your own arm does this: keep your hand flat on a table and move
your elbow. Same hand pose, different arm shape.

---

## 4. Transmission — Gearing

Motors spin fast and weakly. Robots need slow and strong. A **gearbox** trades
one for the other:

```text
Gear ratio 50:1

Speed   ÷ 50     (motor spins 50× for one output turn)
Torque  × 50     (minus friction losses)
```

The costs nobody warns you about:

- **Backlash** — a small amount of free play. The output does not move for the
  first few degrees when you reverse direction. This wrecks precision.
- **Efficiency loss** — a worm gear may return only 40–70% of the input power.
- **Back-drivability** — a high-ratio gearbox cannot be pushed backwards by
  hand. Good for holding a load without power; **dangerous** for a robot that
  works near people, because it cannot yield when it hits something.

That last point is why collaborative robots use low-ratio gearboxes plus torque
sensing, rather than the high-ratio industrial approach.

---

## 5. Controller — the Brain

| Class | Examples | Runs | Use it for |
|---|---|---|---|
| **Microcontroller** | Arduino, ESP32, STM32 | Bare metal | Motor timing, safety cutoffs |
| **Single-board computer** | Raspberry Pi, Jetson | Linux + ROS 2 | Navigation, vision, decisions |
| **Workstation / cloud** | — | Anything | Training models, not real-time control |

Real robots use **two tiers at once**, and the split is deliberate:

```text
Jetson / Raspberry Pi   →  vision, planning, ROS 2      (~10–30 Hz, Linux)
        │  serial / CAN
        ▼
STM32 / Arduino         →  motor control, e-stop        (~1000 Hz, no OS)
```

Linux is **not real-time**. If the vision node stalls for 200 ms, a Linux-driven
motor loop stalls with it, and a moving robot travels a long way in 200 ms. The
microcontroller keeps running regardless — so safety-critical timing lives
there, and only there.

---

## 6. Power — the Most Underrated Subsystem

| Source | Voltage | Notes |
|---|---|---|
| **LiPo** | 3.7 V per cell | High power, light, needs careful charging |
| **Li-ion (18650)** | 3.6 V per cell | Cheap, safer, heavier |
| **NiMH** | 1.2 V per cell | Very safe, low energy density |
| **Lead acid** | 12 V | Cheap, extremely heavy, still used on big AMRs |

The rule beginners learn the hard way: **motors and logic must not share a
weak supply.** A motor starting up briefly draws several times its running
current, the rail voltage dips, and the controller resets in the middle of your
carefully written program. Lesson 3 covers exactly why, and how to prevent it.

---

## How the Parts Talk

| Bus | Speed | Wires | Typical use |
|---|---|---|---|
| **GPIO** | — | 1 | A button, an LED |
| **PWM** | — | 1 | Motor speed, servo angle |
| **UART / serial** | Medium | 2 | Pi ↔ microcontroller, GPS |
| **I²C** | Medium | 2 | IMU, many small sensors on one pair |
| **SPI** | Fast | 4 | Displays, high-rate ADCs |
| **CAN bus** | Fast, robust | 2 | Cars, industrial robots, real AMRs |
| **Ethernet / USB** | Very fast | — | Cameras, lidar |

**CAN** is the one to remember for industry. It was designed for cars: it
survives electrical noise, has no single master, and keeps working when a node
dies. Every serious mobile robot uses it.

---

## 2026 Industry Trend

Actuators are where humanoid robotics is actually being decided. The move is
away from high-ratio geared servos toward **quasi-direct-drive** actuators —
large BLDC motors with a low gear ratio (around 6:1) and current sensing.

The reason is the back-drivability point above: a low-ratio actuator can be
pushed back by an external force, so the robot can *feel* contact through motor
current and yield instead of crushing. That is what makes a 70 kg humanoid safe
enough to stand next to a person.

---

## 🔬 Practical — Take a Robot Apart on Paper

A Webots robot is described in a plain text file listing its components. Read
one:

```bash
python3 world_inspector.py worlds/movebot.wbt
```

```text
  + RectangleArena
        floorSize: 2 2
        wallHeight: 0.08
  + E-puck
        translation: -0.6 -0.6 0
        rotation: 0 0 1 0.785
        controller: "movebot_controller"
```

Map it onto the five subsystems:

- `E-puck` — the **structure**, with a position and rotation in the world
- `controller: "movebot_controller"` — the **controller**, named as a separate
  program
- The E-puck definition itself carries the **actuators** (two wheel motors) and
  **sensors** (8 proximity sensors, a camera)
- **Power** is the one subsystem simulation quietly gives you for free — which
  is exactly why it surprises people on real hardware

Now list all the worlds and inspect a bigger robot:

```bash
python3 world_inspector.py
python3 world_inspector.py worlds/turtlebot_room.wbt
```

---

## 🎯 Interview Question

**What is the difference between a servo motor and a DC motor?**

> A DC motor converts voltage into rotation — you command speed, and you have
> no idea what position it reached unless you add an encoder. A servo bundles a
> DC motor, a gearbox, a position sensor, and a closed-loop controller, so you
> command an angle and it drives itself to that angle and holds it.

<details>
<summary>A harder follow-up: your robot arm sags when it holds a tool. Why?</summary>

Several causes, and a good answer separates them:

- **Gravity torque** — the joint controller has no gravity compensation term, so
  it settles where motor torque balances the load rather than at the commanded
  angle. Fix in software.
- **Backlash in the gearbox** — free play means the output droops before the
  gear teeth re-engage. Fix in hardware, or measure at the output.
- **Insufficient torque** — the motor is at its limit and thermally throttling.
  Fix by re-specifying the actuator.
- **Structural flex** — the link itself is bending. The encoder reads the
  correct joint angle while the tool tip is still in the wrong place.

Note that in the last case **every sensor reports success**. That is the
lesson: joint-space feedback cannot see task-space error.
</details>

---

## 📝 Homework (thinking only)

You are specifying a **warehouse robot** that carries 50 kg shelves across a
concrete floor for an 8-hour shift.

For each of the five subsystems, write one line: what do you choose, and what
breaks if you get it wrong?

<details>
<summary>Some things to think about</summary>

- **Structure** — differential drive for tight aisles; the frame must take 50 kg
  plus shock loads. Too flexible and the lidar shifts, which silently corrupts
  your map.
- **Actuators** — geared BLDC with encoders. Undersize them and the robot stalls
  on a ramp; the motors then draw stall current and overheat within a minute.
- **Sensors** — lidar for navigation, encoders for odometry, IMU for heading,
  bumpers as the last-resort safety layer. Drop the bumper and your safety case
  rests entirely on software.
- **Controller** — a Linux SBC running ROS 2 for planning, plus a microcontroller
  for motor control and the emergency stop. Put the e-stop on Linux and it can
  be delayed by a scheduler.
- **Power** — size the battery for a **full shift plus margin**, because a robot
  that dies mid-aisle blocks the aisle. Separate the motor and logic rails.

The pattern worth noticing: four of the five failure modes are mechanical or
electrical. Very little of robotics failure is bad code.
</details>

---

## 🚀 Next — Lesson 3

**Electronics basics.** Voltage, current, resistance, and power — then the two
things that break beginner robots: motor drivers and shared grounds. This is the
lesson that stops your controller from resetting every time the wheels start.
