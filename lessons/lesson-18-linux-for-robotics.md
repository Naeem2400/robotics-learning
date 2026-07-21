# Lesson 18 — Linux: The Language of Robot Engineers

**Module 11 — Linux for Robotics**

---

## 🎯 Lesson Goal

After this lesson you will understand:

- What Linux is
- What Ubuntu is
- How macOS and Linux are related
- Why robotics runs on Linux
- What role your MacBook plays
- The essential Linux commands

---

## 📖 1. Theory — What Is Linux?

### Technical definition

Linux is an **operating system kernel**. Ubuntu, Debian, Fedora, and other
Linux **distributions** are built on top of it.

### The distinction people get wrong

When someone says *"I use Linux,"* they usually mean they use **Ubuntu** or
another distribution:

```text
Linux Kernel
     │
     ├── Ubuntu
     ├── Debian
     ├── Fedora
     ├── Arch Linux
     └── Linux Mint
```

### What is a kernel?

The kernel is the computer's **manager**. It decides which program gets the
CPU, who gets RAM, and how to talk to hardware.

Like a hotel manager: allocating rooms, directing staff, resolving problems.

```text
Operating System = Kernel + Desktop + Software + Drivers + Tools
```

| OS | Made by |
|---|---|
| Windows | Microsoft |
| macOS | Apple |
| Ubuntu | Linux-based, community + Canonical |

---

## 🍎 2. Your MacBook's Role

You have an Apple M1 running macOS. Here is the good news:

**macOS and Linux both come from the UNIX family.** That is why so many
terminal commands are identical — `pwd`, `ls`, `cd`, `mkdir` all work on both.

This means you can learn real Linux skills on your Mac today, and they will
transfer when you move to Ubuntu or a Jetson.

---

## 🧠 3. Why Robotics Runs on Linux

Why not Windows?

| | |
|---|---|
| ✅ | Stable — runs for months without restarting |
| ✅ | Fast — no heavy desktop consuming resources |
| ✅ | Secure |
| ✅ | Open source — you can inspect and modify anything |
| ✅ | ROS 2 has its best official support on Ubuntu |

There is also a practical reason: a real robot has **no monitor**. You connect
over SSH and the terminal is all you get. An OS built around the command line
is simply a better fit.

### Real companies

| Company | Platform |
|---|---|
| Tesla | Ubuntu / Linux |
| NVIDIA Jetson | Ubuntu |
| Boston Dynamics | Linux-based software |
| Figure AI | Linux ecosystem |

---

## 💻 4. The Commands

You already know these from Lesson 8: `pwd`, `ls`, `cd`, `mkdir`, `touch`.
Here are the rest.

| Command | What it does |
|---|---|
| `clear` | Clear the terminal (or press **Ctrl + L**) |
| `whoami` | Print your username |
| `date` | Current date and time |
| `cal` | Show a calendar |
| `ls -a` | List **all** files, including hidden ones like `.git` |
| `mkdir robot_project` | Create a folder |
| `rmdir robot_project` | Delete an **empty** folder |
| `rm file.py` | Delete a file |
| `cp file1.py file2.py` | Copy |
| `mv old.py new.py` | Move **or rename** |
| `open .` | Open the current folder (macOS) |

### ⚠️ A serious warning about `rm`

**There is no Recycle Bin.** `rm` deletes permanently and immediately. There is
no undo. Think before you press Enter — and be especially careful with `rm -rf`,
which deletes entire folder trees without asking.

### Checking your tools

```bash
python3 --version
pip3 --version
git --version
```

---

## 🔬 5. Practical — What Actually Works on Your Mac

Rather than guessing which commands exist, check:

```bash
bash linux_check.sh
```

[`linux_check.sh`](../linux_check.sh) tests every command from this lesson on
your machine and reports what is available.

### Verified results on this MacBook

**Everything in the table above works**, including `cal`. What is **missing**:

| Missing | What it does | Install |
|---|---|---|
| `tree` | Show folder structure as a tree | `brew install tree` |
| `htop` | Interactive process viewer | `brew install htop` |
| `wget` | Download files (use `curl` instead) | `brew install wget` |
| `xdg-open` | Linux's `open` — **not needed on macOS** | — |

### ⚠️ The trap: same command, different behaviour

This is the part that catches people moving from a Mac to a Jetson. These
commands **exist on both systems but take different options**, because macOS
uses **BSD** tools while Linux uses **GNU** tools:

| Task | Linux (GNU) | macOS (BSD) |
|---|---|---|
| Edit a file in place | `sed -i 's/a/b/' f.txt` | `sed -i '' 's/a/b/' f.txt` |
| Date arithmetic | `date -d '2026-01-01'` | `date -v +1d` |
| File size | `stat -c %s file` | `stat -f %z file` |
| Coloured listing | `ls --color=auto` | `ls -G` |

*These were tested on this machine — the Linux versions genuinely fail on
macOS with "illegal option" errors.* When a script that worked on your Mac
breaks on the robot, this table is the first place to look.

---

## 📁 6. Professional Folder Structure

Robotics engineers do not create random folders:

```text
AI-Robotics/
├── projects/
├── ros2/
├── opencv/
├── ai/
├── datasets/
├── docs/
└── github/
```

### Industry tip

Professional engineers do **not** keep 500 files on the Desktop. Build the
habit of a proper project structure now — this repository is already an
example of one.

### The target workflow

```text
Terminal → VS Code → Git → Python → ROS 2 → Simulation → Jetson → Real robot
```

---

## ⚠️ 7. Common Mistakes

- **Running every command with `sudo`.** `sudo` means "do this as
  administrator." Using it by reflex is how people destroy system files. If a
  command needs `sudo`, understand *why* first.
- **Keeping files on the Desktop.**
- **Not using a virtual environment.**
- **Ignoring Git.**
- **Assuming a macOS script will run on Linux.** See the BSD/GNU table above.

---

## 🎯 8. Interview Question

**Why does robotics use Ubuntu/Linux?**

> Because Linux is stable, fast, and open source, and it is the primary
> supported platform for ROS 2. That is why both research and industry rely on
> it.

<details>
<summary>Follow-up: what is the difference between Linux and Ubuntu?</summary>

Linux is the **kernel** — the core that manages CPU, memory, and hardware.
Ubuntu is a **distribution**: the Linux kernel packaged together with a
desktop, drivers, a package manager, and tools. You cannot really "install
Linux" by itself; you install a distribution that contains it.
</details>

---

## 💡 9. 2026 Industry Note

Robotics is no longer just Linux + ROS 2. Engineers use:

Python · C++ · Docker · Git · VS Code · CUDA (NVIDIA GPUs) ·
AI frameworks (PyTorch, ONNX) · ROS 2

**Linux is the foundation under all of it.**

---

## 🛣️ Progress

```text
Robot basics ✅   Electronics ✅   Sensors ✅   Computer Vision ✅
YOLO ✅   ROS 2 ✅   Linux ✅
```

Next comes the real engineering toolchain.

---

## 🚀 Next — Lesson 19: Git & GitHub for Robotics Engineers

Important because every robotics company uses Git, every AI engineer needs
version control, and your portfolio lives on GitHub. We will cover branches,
commits, pull requests, and project versioning.

> You already have a repository doing exactly this:
> **github.com/Naeem2400/robotics-learning** — every lesson's code has been
> committed to it as we went. Lesson 19 will explain what has been happening
> behind those commits.

After that: **Docker**, **ROS 2 development**, and **Webots simulation**.
