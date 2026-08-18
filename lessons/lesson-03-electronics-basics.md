# Lesson 3 — Electronics Basics

**Module 3 — Electronics Basics**

> **Golden rule:** Current is what actually breaks things. Voltage decides
> whether a component works; current decides whether it survives.

---

## Lesson Objectives

After this lesson you will understand:

- Voltage, current, and resistance, and how Ohm's law connects them
- How to calculate power and battery runtime for a real robot
- Why a microcontroller cannot drive a motor directly
- What PWM is and how it controls speed
- The three wiring mistakes that kill beginner robots

---

## The Water Analogy

Electricity is invisible, so use the pipe:

```text
   Voltage (V)  = water PRESSURE     — how hard it is pushed
   Current (I)  = water FLOW RATE    — how much is actually moving
   Resistance(R)= pipe NARROWNESS    — what restricts the flow
```

| Quantity | Symbol | Unit | Measured with |
|---|---|---|---|
| Voltage | V | volts (V) | Multimeter **across** a component |
| Current | I | amperes (A) | Multimeter **in line** with the circuit |
| Resistance | R | ohms (Ω) | Multimeter, power off |
| Power | P | watts (W) | Calculated |

The analogy pays off immediately: high pressure with a closed tap moves no
water. A 240 V supply touching a perfect insulator passes no current and does
nothing. **Voltage alone is not what hurts you or your components — current is.**

---

## Ohm's Law

```text
V = I × R

I = V / R
R = V / I
```

**Worked example — sizing a resistor for an LED.**

An LED needs about 2 V across it and 20 mA (0.02 A) through it. Your supply is
5 V. The resistor must drop the leftover 3 V:

```text
V across resistor = 5 V − 2 V = 3 V
R = V / I = 3 / 0.02 = 150 Ω
```

Connect the LED without that resistor and nothing limits the current. The LED
conducts almost freely, current spikes, and it burns out — often in under a
second. Same voltage, no resistance, dead part.

---

## Power and Heat

```text
P = V × I

and by substituting Ohm's law:

P = I² × R
```

Power is measured in watts, and in a robot **watts you did not plan for come out
as heat**.

| Device | Voltage | Current | Power |
|---|---|---|---|
| LED | 2 V | 0.02 A | 0.04 W |
| Raspberry Pi 5 | 5 V | 3 A | 15 W |
| Small DC motor (running) | 6 V | 0.5 A | 3 W |
| Same motor (**stalled**) | 6 V | 2.5 A | **15 W** |

Look at the last two rows. A blocked motor draws roughly five times its running
current and dissipates all of it as heat, because it is producing no motion. A
motor that jams against a wall is a **heater** — and it will destroy a driver
rated for the running current within a minute or two.

Note the `I² × R` form: doubling the current *quadruples* the heat. This is why
current, not voltage, is the number to watch.

---

## Batteries and Runtime

A cell's **nominal voltage** depends on its chemistry, and cells in series add:

```text
1 LiPo cell (1S)  = 3.7 V nominal   (4.2 V full,  ~3.0 V empty)
3 cells   (3S)    = 11.1 V nominal  (12.6 V full)
4 cells   (4S)    = 14.8 V nominal  (16.8 V full)
```

**Capacity** is given in mAh (milliamp-hours) or Ah. A 2200 mAh battery supplies
2200 mA for one hour, or 1100 mA for two hours.

### Worked example — will this robot survive a demo?

Your robot draws:

```text
Raspberry Pi + camera      600 mA
2 drive motors, average    900 mA
Lidar                      300 mA
                        ─────────
Total                     1800 mA
```

With a 5200 mAh battery:

```text
Ideal runtime = 5200 / 1800 = 2.9 hours
```

Now apply reality. Never plan on the ideal number:

```text
Realistic ≈ 2.9 × 0.75 ≈ 2.1 hours
```

The 0.75 accounts for regulator losses, voltage sag under load, and the fact
that you must stop at ~20% charge — draining a LiPo flat permanently damages it.

### C-rating

The **C-rating** is the maximum safe continuous discharge, as a multiple of
capacity:

```text
5200 mAh = 5.2 Ah,  rated 25C
Max continuous current = 5.2 × 25 = 130 A
```

Exceed it and the battery heats, swells, and — with LiPo — can catch fire.
Cheap batteries routinely overstate this number.

---

## Why a Microcontroller Cannot Drive a Motor

This is the single most common beginner mistake.

```text
Arduino GPIO pin   →  max ~20 mA  (40 mA absolute, per pin)
Small DC motor     →  needs 500–2500 mA
```

The pin can supply roughly **1%** of what the motor needs. Wire a motor straight
to a GPIO pin and you destroy the pin, usually the whole microcontroller.

The fix is a **motor driver** — the GPIO pin carries a *signal*, and the driver
switches the *power*:

```text
Battery ──────────────┐
                      ▼
Controller ──signal──▶ MOTOR DRIVER ──power──▶ Motor
  (20 mA)              (L298N, TB6612,
                        DRV8833, VESC)
```

The controller says what to do. The driver does the work. Keep those two
sentences separate in your head and most wiring questions answer themselves.

### The H-bridge

A motor driver contains an **H-bridge**: four switches that let current flow
through the motor in either direction.

```text
Switches A+D closed  →  current flows left-to-right   →  forward
Switches B+C closed  →  current flows right-to-left   →  reverse
All open             →  coast
A+C closed           →  short across the motor        →  brake
```

Closing A and B at once connects battery positive straight to ground through
the driver. This is called **shoot-through**, and it destroys the driver
instantly. Real drivers insert a few nanoseconds of *dead time* to prevent it —
which is one good reason not to build your own H-bridge out of loose
transistors.

---

## PWM — Controlling Speed Without Wasting Power

A digital pin can only be fully on or fully off. So how do you run a motor at
half speed?

**Pulse Width Modulation:** switch the pin on and off very fast, and vary the
fraction of time it spends on.

```text
100% duty   ████████████████████   full speed
 75% duty   ███████████████░░░░░   three-quarter
 50% duty   ██████████░░░░░░░░░░   half speed
 25% duty   █████░░░░░░░░░░░░░░░   slow
  0% duty   ░░░░░░░░░░░░░░░░░░░░   stopped
```

The motor's inertia and coil inductance smooth the pulses into what is
effectively an average voltage. Typical PWM frequencies are 1–20 kHz — above
~20 kHz because that puts the switching whine above human hearing, which is why
a cheap robot audibly sings and an expensive one does not.

**Why not just use a resistor to lower the voltage?** Because a resistor turns
the difference into heat (`P = I² × R`). PWM switches are either fully on (near
zero resistance) or fully off (no current), so they dissipate almost nothing.
PWM is efficient; resistive control is a space heater.

> ⚠️ **PWM duty cycle is not speed.** 50% duty on an unloaded motor is fast;
> 50% duty on a motor pushing a heavy robot up a ramp may not move at all. If
> you need actual speed, you need an encoder and a closed loop — which is why
> Lesson 12's sensors matter.

---

## The Three Mistakes That Kill Beginner Robots

### 1. No common ground

```text
❌  Battery ─── Motor driver          (grounds not connected)
    USB ─────── Controller

✅  All grounds tied together
```

A signal voltage is meaningless without a shared reference. With separate
grounds, your 3.3 V "high" is measured against a different zero, and the driver
sees noise. Symptom: the motor twitches randomly, or ignores commands entirely.
**Connect every ground together.** This is not optional.

### 2. Brownout from motor inrush

A motor starting up draws its stall current for a moment. That surge drags the
shared rail down, the controller's supply dips below its minimum, and it resets
— mid-program.

```text
Symptom: the robot reboots every time the wheels start.
```

Three fixes, in order of effectiveness:

- Power the motors from a **separate supply** to the logic (grounds still
  common)
- Add a large **capacitor** (470–1000 µF) across the motor supply to absorb the
  surge
- Ramp the PWM up over ~200 ms instead of jumping from 0 to full

### 3. Mismatched logic levels

```text
Raspberry Pi, ESP32, Jetson  →  3.3 V logic
Arduino Uno, many sensors    →  5 V logic
```

Feeding 5 V into a 3.3 V input can destroy it. The reverse — 3.3 V into a 5 V
input — often *appears* to work, then fails intermittently at temperature,
which is far worse than failing outright. Use a **level shifter** and check the
datasheet before connecting two boards.

### And one for hardware safety

Motors are inductive. When you switch one off, the collapsing magnetic field
generates a reverse voltage spike — **back-EMF** — that can be many times the
supply voltage. Motor drivers include **flyback diodes** to clamp it. If you
ever switch an inductive load with a bare transistor, you must add that diode
yourself.

---

## 2026 Industry Trend

Robot power systems are converging on **higher voltages**: 24 V and 48 V buses
instead of 12 V.

The reason falls straight out of `P = V × I`. To deliver the same power at
double the voltage, you need half the current — which means thinner cables, less
resistive loss, and much less heat. Humanoids run 48 V bus systems for exactly
this reason. Meanwhile smart **BMS** (battery management systems) report cell
health over CAN, so the robot can plan around its own remaining charge instead
of dying unexpectedly.

---

## 🔬 Practical — Size a Battery for the MoveBot

No hardware needed. Do this with a calculator and the numbers below.

Your robot has: a Raspberry Pi 4 (700 mA), a camera (250 mA), two motors
averaging 400 mA each, and an IMU (10 mA). You need **90 minutes** of runtime.

1. Total the current draw.
2. Convert 90 minutes to hours.
3. Calculate the ideal capacity needed (`current × hours`).
4. Divide by 0.75 for real-world losses and the 20% reserve.
5. Pick the next standard size up from: 2200, 3300, 5200, 8000 mAh.

<details>
<summary>Check your answer</summary>

```text
1. 700 + 250 + 400 + 400 + 10 = 1760 mA
2. 90 minutes = 1.5 hours
3. 1760 × 1.5 = 2640 mAh   (ideal)
4. 2640 / 0.75 = 3520 mAh  (realistic requirement)
5. Next size up → 5200 mAh
```

Notice that the naive answer (2640, so "a 3300 mAh pack is fine") leaves you
short. The margin is not padding — it is the regulator losses and the charge you
must not use. A robot specified on the ideal number dies before the demo ends.

**Bonus:** if those motors stall against a wall at 2000 mA each, total draw
jumps to about 4960 mA and the same pack lasts roughly 47 minutes at best. Stall
current is not a corner case; it is what happens every time the robot gets stuck.
</details>

---

## 🎯 Interview Question

**Why can't you connect a motor directly to a microcontroller pin?**

> A GPIO pin can source about 20 mA, while even a small DC motor needs several
> hundred to a few thousand. The pin cannot supply the current and is destroyed.
> You use a motor driver: the controller sends a low-current signal, and the
> driver switches the high-current path from the battery.

<details>
<summary>A harder follow-up: your robot resets whenever the motors start. Diagnose it.</summary>

The symptom points at **brownout**: motor inrush current pulls the shared supply
rail below the controller's minimum operating voltage, and it resets.

How to confirm rather than guess:

1. Put a multimeter (better, a scope) on the controller's supply and watch it
   during motor start. A visible dip confirms the diagnosis.
2. Run the motors from a bench supply while the controller stays on USB, with
   grounds common. If the resets stop, it is the shared rail.

Fixes in order: separate the motor and logic supplies, add bulk capacitance
across the motor rail, and ramp PWM instead of stepping it.

The wrong instinct — and the common one — is to start rewriting the firmware.
No amount of code fixes a voltage that fell below the controller's minimum.
</details>

---

## 📝 Homework (thinking only)

A robot arm holds a 2 kg tool. The joint motor is rated 12 V, 3 A stall,
0.8 A running.

1. What power does it dissipate while running normally?
2. What power if the arm jams against a table and stalls?
3. Your motor driver is rated for 2 A continuous. What happens, and how long do
   you think you have?
4. What would you add to the system so this never destroys the driver?

<details>
<summary>Some things to think about</summary>

```text
1. P = 12 × 0.8 = 9.6 W
2. P = 12 × 3.0 = 36 W        — nearly 4× the heat, in a package sized for 9.6 W
3. 3 A through a 2 A driver: it overheats. A good driver has thermal shutdown
   and cuts out (the arm goes limp — itself a hazard with a 2 kg tool). A cheap
   one has no protection and the output stage fails, often shorted-on, which
   means the motor runs at full power with no way to stop it in software.
```

For (4), a layered answer is the strong one:

- **Current sensing** in the driver, with a firmware limit that cuts power above
  a threshold — this also gives you free collision detection
- A **stall timeout**: if commanded to move but the encoder reports no motion for
  200 ms, stop
- A **mechanical fuse** or slip clutch as the last line of defence
- Specify the driver for **stall current**, not running current

That last point is the real lesson of this module: components are sized for the
worst case, not the typical one.
</details>

---

## 🚀 Next — Lesson 4

**Python for Robotics.** With the hardware understood, we move to the code that
drives it: variables, decisions, and the sense-think-act loop written properly.
The lesson notes for this module are in the main
[README](../README.md#python-for-robotics--variables--decisions), and the code is in
[`robot.py`](../robot.py).
