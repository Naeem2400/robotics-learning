# Lesson 8 — The Professional Robotics Workspace

**Module 5 — Professional Development Environment**

---

## ⚠️ An Important Shift

From here on, we are not just writing programs. We are building an environment
the way a **real robotics engineer** does.

When you join a robotics company or internship, their workflow looks like this:

```text
MacBook
    │
    ▼
VS Code
    │
    ▼
Git
    │
    ▼
Python
    │
    ▼
ROS 2
    │
    ▼
Simulation
    │
    ▼
Real Robot
```

Every layer sits on the one above it. That is why **environment setup comes
first** — you cannot run a simulation before you can navigate a folder.

---

## What We Will Install

You already have:

- ✅ VS Code
- ✅ Python
- ✅ GitHub

In this module we add and verify:

- Homebrew
- Git
- Docker
- Webots
- Terminal fundamentals

---

## Step 1 — What Is a Terminal?

### Definition

The terminal is an application where you control the computer by typing **text
commands** instead of clicking.

Normally you click with a mouse. In the terminal, you type:

```bash
pwd
```

and the computer answers:

```text
/Users/naeem
```

### An analogy

| | |
|---|---|
| **Mouse** | An automatic car — easy, but limited control |
| **Terminal** | A manual sports car — steeper learning curve, full control |

Professional developers live in the terminal, because it is faster, scriptable,
and it is the *only* interface you get when you SSH into a robot.

That last point matters. A real robot has no monitor and no mouse. When you
connect to a robot's onboard computer, the terminal is all there is.

---

## Step 2 — Open the Terminal

On macOS:

```text
⌘ + Space  →  type "Terminal"  →  Enter
```

---

## Step 3 — Your First Command

```bash
pwd
```

Output:

```text
/Users/YourName
```

### What does `pwd` mean?

**P**rint **W**orking **D**irectory — *"which folder am I in right now?"*

The terminal always has a current location. `pwd` tells you where you are
standing.

---

## Step 4 — List the Contents

```bash
ls
```

This shows every file and folder inside your current location:

```text
Desktop
Documents
Downloads
Movies
Pictures
```

**`ls`** = **l**i**s**t.

> **Tip:** `ls -l` shows details (size, date, permissions) and `ls -a` also
> shows hidden files — the ones starting with a dot, like `.git`.

---

## Step 5 — Move to the Desktop

```bash
cd Desktop
```

Confirm where you landed:

```bash
pwd
```

```text
/Users/YourName/Desktop
```

### What does `cd` mean?

**C**hange **D**irectory — move from one folder into another.

> **Tip:** `cd ..` goes up one level to the parent folder, and `cd` on its own
> takes you straight home.

---

## Step 6 — Create a Folder

```bash
mkdir robotics_bootcamp
```

**`mkdir`** = **m**a**k**e **dir**ectory.

---

## Step 7 — Enter the Folder

```bash
cd robotics_bootcamp
```

---

## Step 8 — Create a Python File

```bash
touch robot.py
```

### What does `touch` do?

It creates an empty file. (Its original purpose was updating a file's
timestamp — hence the name — but creating empty files is what it is used for
day to day.)

---

## Step 9 — Check the Folder

```bash
ls
```

```text
robot.py
```

---

## Step 10 — Open VS Code

```bash
code .
```

The `.` means *"this folder"* — so this opens your current folder in VS Code.

### If you see an error

```text
command not found: code
```

No problem. Inside VS Code:

```text
⌘ + Shift + P  →  search: Shell Command: Install 'code' command in PATH
```

Click it, then close and reopen your terminal and try `code .` again.

---

## Today's Goal

You have learned six commands:

| Command | Meaning | Purpose |
|---------|---------|---------|
| `pwd` | print working directory | Where am I? |
| `ls` | list | What is here? |
| `cd` | change directory | Go somewhere |
| `mkdir` | make directory | Create a folder |
| `touch` | create empty file | Create a file |
| `code .` | — | Open the current folder in VS Code |

You will use these every single day for the rest of your career.

---

## Mini Challenge

Type these yourself — **no copy-paste.** Muscle memory is the whole point.

```bash
mkdir ai_robot
cd ai_robot
touch main.py
ls
pwd
```

If everything worked, `ls` shows:

```text
main.py
```

---

## Homework

Reply with just three things:

1. The output of `pwd`
2. The output of `ls`
3. Did `code .` work? (Yes / No)

You can also run the environment checker in this repository to see your whole
toolchain at once:

```bash
python3 setup_check.py
```

---

## 📌 A Note on Where This Is Going

This is not just a robotics course. It is an **AI Robotics Engineer Bootcamp**.

The end goal is not simply making a robot move. We will eventually build:

- 🤖 AI Voice Robot
- 👁️ Computer Vision Robot
- 🚗 Autonomous Navigation Robot
- 🦾 Robot Arm Controller
- 📦 Warehouse Robot
- 🧍 Humanoid Assistant
- 🧠 AI Agent + Physical Robot Integration

These are the same skills used across the industry — at Tesla, Figure AI,
Agility Robotics, Unitree, and in the NVIDIA robotics ecosystem.

---

## 🚀 Next — Lesson 9

Once you are comfortable with these commands, we install:

- Homebrew
- Docker
- Webots (robot simulator)

Then we run **your first virtual robot** on screen — with **no hardware to
buy**. That will be the first real simulation project of your robotics journey.
