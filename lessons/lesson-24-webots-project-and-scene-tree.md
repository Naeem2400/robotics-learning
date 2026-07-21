# Lesson 24 — The Webots Project and Scene Tree

**Project 1 — MoveBot**

> Before writing controller code, understand **where that code lives** and
> **what the world is made of**. Ten minutes here saves hours of "why can't
> Webots find my controller?"

---

## 🎯 Lesson Goal

- Create a Webots project properly
- Understand the Scene Tree
- Understand nodes and fields
- Know the naming rules Webots enforces silently

---

## 📁 1. Creating the Project

In Webots: **File → New → New Project Directory**, name it `MoveBot`, then
create a new world and save it as `MoveBot.wbt`.

Webots creates this:

```text
MoveBot/
├── controllers/
└── worlds/
    └── MoveBot.wbt
```

### ⚠️ Two naming rules Webots will not warn you about

1. **The folders must be called `worlds/` and `controllers/`** at the project
   root. Not `world/`, not `Controllers/`.
2. **A controller folder must exactly match its Python file:**

```text
controllers/movebot_controller/movebot_controller.py   ✅
controllers/movebot/controller.py                      ❌ silently ignored
```

Break either rule and Webots does not error — the robot simply sits still.
This is the single most common beginner problem, and now you know it.

---

## 🌳 2. The Scene Tree

The Scene Tree panel lists everything in your world:

```text
+ WorldInfo          simulation settings
+ Viewpoint          where the camera is
+ TexturedBackground the sky
+ RectangleArena     the floor and walls
+ E-puck             the robot
```

### Nodes and fields

- A **node** is an object — a robot, a floor, a box, a light
- A **field** is a property of that node — its position, its size, its
  controller

```text
E-puck                        <- node
   translation -0.6 -0.6 0    <- field
   rotation 0 0 1 0.785       <- field
   controller "movebot..."    <- field
```

Selecting a robot and changing `controller` in the Scene Tree is how you tell
it which program to run.

---

## 🔬 3. Practical — A World Is Just a Text File

This is the insight that makes Webots click:

```bash
python3 world_inspector.py worlds/movebot.wbt
```

```text
  + WorldInfo
        title: "MoveBot"
  + RectangleArena
        floorSize: 2 2
        wallHeight: 0.08
  + E-puck
        translation: -0.6 -0.6 0
        controller: "movebot_controller"
```

[`world_inspector.py`](../world_inspector.py) reads the `.wbt` file with plain
Python and prints the same tree Webots shows you. **The 3D world is a text
file.** Open `worlds/movebot.wbt` in VS Code and you will see exactly these
lines.

Run it with no arguments to list every world in this project:

```bash
python3 world_inspector.py
```

### Why this matters

Because the world is text:

- It can be **version controlled** — you can `git diff` a world change
- You can edit it in VS Code instead of clicking through panels
- You can **generate** worlds with a script (we did exactly that for the
  furnished room in Lesson 10)

---

## 📦 4. EXTERNPROTO — Where Objects Come From

At the top of every world file:

```text
EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/.../E-puck.proto"
```

Webots does **not** ship most objects inside the app. It downloads their
definitions from GitHub the first time a world uses them, then caches them.

Two practical consequences:

- **The first load of a new world needs internet.** After that it works
  offline.
- A world referencing many objects is slow to open the first time and fast
  afterwards.

---

## 🔧 5. Hidden Fields

Open a world you have already run and you will see lines like:

```text
hidden position_0_0 267.6469839883553
hidden linearVelocity_0 -5.57e-08 ...
```

Webots writes these automatically — they record where everything ended up when
the simulation last ran. **You never write them by hand**, and they are why a
world file looks different after you press Run.

---

## ⚠️ 6. Common Mistakes

- **Controller folder name ≠ file name** — silent failure
- **Editing a `.wbt` while Webots has it open** — Webots overwrites your
  changes when it saves. Close or reload first
- **Committing `.wbproj` files** — these store your window layout, not your
  world. They belong in `.gitignore`
- **Expecting a world to open offline the first time** — EXTERNPROTOs need to
  download once

---

## 🎯 7. Interview Question

**What is the difference between a world and a controller in Webots?**

> A world describes the environment and the robots in it — geometry, physics,
> and sensors. A controller is the program that runs on a robot and decides
> what it does. One world can contain several robots, each with its own
> controller.

---

## 🚀 Next — Lesson 25: Writing the Controller

Now that the project structure makes sense, we write the Python that makes
MoveBot move.
