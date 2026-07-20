# 🤖 AI Robotics Bootcamp (2026 Industry Edition)

## Course Progress

| | Module | Lesson notes |
|---|---|---|
| ✅ | 1 — Robotics Introduction | — |
| ✅ | 2 — Robot Components | — |
| ✅ | 3 — Electronics Basics | — |
| ✅ | 4 — Python for Robotics (Basic) | below ↓ |
| 🔄 | 5 — Professional Development Environment | [Lesson 8 — Workspace](lessons/lesson-08-professional-workspace.md) · [Lesson 9 — Simulation](lessons/lesson-09-robot-simulation.md) |

**Check your toolchain at any time:** `python3 setup_check.py`

---

# Python for Robotics — Variables & Decisions

*Module 4*

You already know Python. Robotics Python is a different *way of thinking*, not a different language.

In this lesson we learn to think like a robot.

---

## 1. What Is Robot Programming?

A normal program is a straight line:

```
User Input  →  Process  →  Print Result
```

A robot program is a loop that touches the physical world:

```
Sensor  →  Decision  →  Motor  →  Movement
              ↑                       │
              └───────── feedback ────┘
```

That cycle — **sense, decide, act** — is the core concept of robotics.
Every robot, from a $30 line follower to a Tesla, runs this loop.

---

## 2. Variables

### Definition

A variable is a labelled box that stores a piece of data.

Think of the storage boxes in a house: one box holds shoes, another holds
books, another holds clothes. Each box has a label so you know what is inside.
Python works the same way — the label is the variable name.

### Examples

```python
battery = 90            # robot battery is at 90%
distance = 25           # wall is 25 cm away
robot_name = "Atlas"    # the robot's name
```

### A real robot example

The ultrasonic sensor reports a reading of 10 cm. In Python:

```python
distance = 10
```

The robot can now *decide* what to do with that number.

---

## 3. Decision Making

```python
distance = 10

if distance < 20:
    print("Stop")
```

In plain English: **if the wall is closer than 20 cm, stop the robot.**

This is where robot intelligence begins.

### Real world: a Tesla

```
Camera  →  Distance estimate  →  Python/C++ logic  →  Brake
```

Same logic, more sensors.

### Real world: a robot vacuum

```python
distance = 5

if distance < 15:
    print("Turn left")
```

---

## 4. Data Types a Robot Uses

| Type | Meaning | Robot example |
|------|---------|---------------|
| `int` | whole number | `wheels = 4` |
| `float` | decimal number | `distance = 1.25` (metres) |
| `bool` | True / False | `obstacle = True` |
| `str` | text | `robot_name = "Optimus"` |

### Boolean — the robot's yes/no questions

A robot constantly asks yes/no questions: *Is there an obstacle? Is the
battery low? Is the arm holding something?*

```python
obstacle = True

if obstacle:
    print("Stop robot")
```

Note: `if obstacle:` already means *if obstacle is True* — no `== True` needed.

### String — the robot can speak

```python
robot_name = "Optimus"
voice = "Welcome"
```

### Float — precise measurement

Distances and speeds are rarely whole numbers.

```python
distance = 1.25   # metres
```

### Integer — countable things

```python
wheels = 4
```

---

## 5. A Robot's State in Variables

```python
battery = 95          # percent
temperature = 30      # degrees Celsius
speed = 1.5           # metres per second
robot_name = "NaeemBot"
obstacle = False
```

Together these variables describe **the robot state** at one moment in time.
Keep this idea in mind — it becomes important in ROS 2.

---

## 6. Practical Projects

### Project 1 — Robot identity

Create a file called `robot.py`:

```python
robot_name = "NaeemBot"
battery = 100
speed = 1.2

print(robot_name)
print(battery)
print(speed)
```

Output:

```
NaeemBot
100
1.2
```

### Project 2 — Battery drain

```python
battery = 80
battery = battery - 10
print(battery)
```

Output:

```
70
```

The robot has used 10% of its battery. The right-hand side is calculated
first, then stored back into the same box.

### Project 3 — Obstacle check

```python
distance = 15

if distance < 20:
    print("Robot stop")
else:
    print("Move")
```

Output:

```
Robot stop
```

---

## 7. Think About It 🤔

What is the output if `distance = 50`?

<details>
<summary>Answer</summary>

```
Move
```

50 is not less than 20, so the `else` branch runs.
</details>

---

## 8. Mini Challenge

Write this yourself: if the robot's battery is below 20%, print

```
Battery low
Go charging
```

otherwise print

```
Keep working
```

Hint: start with `battery = 15`.

A worked solution is in [`challenge_solution.py`](challenge_solution.py) —
try it on your own first.

---

## 💡 One Important Note

This course does not teach syntax alone. Every line comes with the robotics
reason behind it.

When we move to **ROS 2**, these same variables become **topics**, **sensor
messages**, and **robot state**. `distance = 10` becomes a subscriber reading
a `LaserScan` message. The thinking stays identical; only the plumbing grows.

---

## 📚 Homework

1. Create `robot.py`.
2. Run all three projects yourself.
3. Solve the battery challenge.
4. Push the code to a GitHub repository named `robotics-learning`. ✅ (this repo)

---

## Files in This Repository

| File | Description |
|------|-------------|
| [`robot.py`](robot.py) | All lesson examples in one runnable script |
| [`robot_lesson.ipynb`](robot_lesson.ipynb) | The same lesson as an interactive notebook |
| [`challenge_solution.py`](challenge_solution.py) | Solution to the battery mini challenge |
| [`setup_check.py`](setup_check.py) | Checks your robotics toolchain (Lesson 8) |
| [`lessons/`](lessons/) | Lesson notes from Module 5 onward |
| [`controllers/`](controllers/) | Webots robot controllers (run from inside Webots) |

### How to run

```bash
python3 robot.py
python3 challenge_solution.py

# for the notebook
pip install notebook
jupyter notebook robot_lesson.ipynb
```
