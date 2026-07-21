# Lesson 11 — Object-Oriented Programming (OOP) for Robotics

**Module 5 — Professional Development Environment**

> This is the most important programming lesson in the course.

Once OOP is solid, all of these become much easier to understand:

✅ ROS 2 ✅ Robot SDKs ✅ NVIDIA Isaac ROS ✅ Drone programming
✅ AI agents ✅ Humanoid robots

---

## 📌 A Note on How We Learn Here

This course uses **spiral learning** — the approach used at MIT and Stanford.
You get an overview first, then every concept returns in more depth during real
projects. So if you have not finished an earlier challenge yet, do not worry.
Keep moving; it will come back naturally when we build a real robot.

---

## Two Worlds of Programming

### 1. Procedural programming

```python
battery = 100
print(battery)
```

All the code sits in one place. Fine for small programs.

### 2. Object-oriented programming

Here we represent **real-world things** in code. A real robot has parts:

```text
Robot
│
├── Camera
├── LiDAR
├── Battery
├── Wheels
├── Arm
└── Brain
```

In OOP, each of those becomes its own object with its own job — exactly like a
car company builds an engine, wheels, doors, and steering as separate parts.

---

## What Is a Class?

A **class** is a **blueprint**.

Before building a house, an engineer draws a blueprint. From that one blueprint
you can build a hundred houses. In programming, that blueprint is a class.

## What Is an Object?

An **object** is the actual thing built from the blueprint.

```text
Toyota Corolla design  →  factory  →  a real car
        (class)                        (object)
```

---

## Building a Robot Class

```python
class Robot:
    pass
```

Right now this is only a design. Nothing exists yet.

```python
robot1 = Robot()      # now one robot exists
robot2 = Robot()      # now two robots exist
```

Both were built from the same design.

### Giving the robot properties

A real robot has a name, a battery, a speed:

```python
class Robot:
    def __init__(self, name, battery):
        self.name = name
        self.battery = battery
```

**`__init__`** runs automatically whenever a new robot is created — like a
factory assembling the robot. **`self`** means *this particular robot*, which
is how `robot1` keeps its own name separate from `robot2`.

```python
robot1 = Robot("Atlas", 100)
robot2 = Robot("Optimus", 80)

print(robot1.name)    # Atlas
print(robot2.name)    # Optimus
```

Two objects, same class, different data.

### Giving the robot actions

A robot does not only hold data — it *does* things. An action inside a class is
called a **method**.

```python
class Robot:
    def __init__(self, name, battery):
        self.name = name
        self.battery = battery

    def move(self):
        print(f"{self.name} is moving")

    def speak(self):
        print("Hello human")

    def charge(self):
        self.battery = 100
        print("Battery full")
```

```python
robot = Robot("NaeemBot", 60)
robot.move()          # NaeemBot is moving
robot.charge()        # Battery full
print(robot.battery)  # 100
```

Notice `charge()` **changed the robot's own data**. That is the heart of OOP:
data and the actions that affect it live together in one place.

---

## Where This Is Used in Robotics

Real robot software is organised exactly like this:

```text
Robot
│
├── Camera        ├── GPS
├── Motor         ├── IMU
├── Battery       ├── LiDAR
└── RobotBrain
```

Each class does its own job. This is why large robotics projects stay
manageable. A Boston Dynamics robot is not one file — it is **hundreds of
classes** and hundreds of thousands of lines of code. Without OOP that would be
impossible to maintain.

This idea has a name: **composition** — a robot *has a* battery, *has a* lidar.
You will see it again immediately in ROS 2, where each part becomes a node.

---

## Mini Project

The runnable version is [`robot_oop.py`](../robot_oop.py) in this repository.

```python
class Robot:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, I am {self.name}")


robot = Robot("NaeemBot")
robot.greet()          # Hello, I am NaeemBot
```

> **Note:** the lesson calls this file `robot.py`, but this repository already
> uses that name for the Module 4 variables lesson, so it is saved here as
> `robot_oop.py`.

---

## 🧠 Interview Question

**What is the difference between a class and an object?**

- **Class** = the blueprint (the design)
- **Object** = the actual thing built from it

*Class = the robot's design. Objects = Atlas, Optimus, Spot — real robots built
from that design.*

<details>
<summary>A follow-up they often ask: what is <code>self</code>?</summary>

`self` refers to *the specific object the method is being called on*. When you
write `robot1.charge()`, Python passes `robot1` in as `self`, so the method
changes `robot1`'s battery and not `robot2`'s. One class, many objects, each
with its own data.
</details>

---

## ⚡ Common Mistakes

- **Forgetting `self`** in a method definition — `def move():` instead of
  `def move(self):` raises a `TypeError`.
- **Forgetting `self.`** when storing data — `name = name` creates a temporary
  variable that vanishes; you need `self.name = name`.
- **Confusing the class with the object** — `Robot` is the design;
  `Robot("Atlas", 100)` is a real robot. Calling `Robot.move()` without an
  object will fail.

---

## 🎯 Next — Lesson 12

**Sensors — the robot's eyes, ears, and skin.** We will look in detail at the
camera, LiDAR, ultrasonic sensor, IMU, GPS, encoders, touch sensors, and force
sensors, and answer the key question: **how does a robot know what is happening
around it?**

This is the foundation of AI robotics, because without sensors a robot is
**blind and deaf**.
