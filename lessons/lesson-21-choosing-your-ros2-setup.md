# Lesson 21 — Choosing Your ROS 2 Setup

**Module 13 — Docker** *(bridge lesson before ROS 2 practical)*

> Before writing ROS 2 code, you must decide **where it will run**. Choose
> wrong on a MacBook Air and you will fight your laptop instead of learning
> robotics.

---

## 🎯 Lesson Goal

- Why ROS 2 is awkward on macOS
- The four possible setups and their real costs
- Which one fits an 8 GB MacBook Air M1
- How the choice carries over to a Jetson later

---

## 📖 1. The Problem

ROS 2's primary supported platform is **Ubuntu Linux**. macOS support exists
but is *experimental*: it means building from source, which takes hours and
frequently breaks after an OS update.

So you need Linux somehow. There are four ways.

---

## ⚖️ 2. The Four Options

### Option A — Native Ubuntu (dual boot)

Install Ubuntu alongside macOS on the same Mac.

| ✅ | ❌ |
|---|---|
| Full speed, full hardware access | **Not realistically possible on Apple Silicon.** Asahi Linux exists but is incomplete, and ROS 2 support on it is not a supported path |
| The industry standard on Intel/AMD machines | You must reboot to switch |

**Verdict for your machine: not viable.**

### Option B — Ubuntu in a virtual machine

Run Ubuntu inside macOS using UTM or Parallels.

| ✅ | ❌ |
|---|---|
| Full Ubuntu desktop, closest to a real robot | Needs 4 GB+ RAM for the VM alone |
| Good for learning the Ubuntu environment | Graphics acceleration is limited — simulators run poorly |

**On your machine:** you have **8 GB total**. macOS itself wants ~3–4 GB. Give
a VM 4 GB and both systems are starved, and you will be swapping to disk
constantly. It *works*, but it is unpleasant.

### Option C — Docker

Run ROS 2 inside a container on macOS.

| ✅ | ❌ |
|---|---|
| Much lighter than a VM — no second desktop | GUI tools (RViz, Gazebo) need extra setup |
| **The same container runs on your Jetson later** | Some ROS 2 images are x86-only and emulate slowly |
| Matches how industry actually ships robotics software | Docker Desktop needs ~2.5 GB disk |

### Option D — Stay on macOS

Skip ROS 2 for now; keep using Python and Webots directly.

| ✅ | ❌ |
|---|---|
| Zero setup cost — works today | No real ROS 2 |
| Webots, OpenCV, and Python all run natively | You postpone an essential skill |

---

## 💻 3. Your Machine, Measured

These are this machine's actual specifications, not estimates:

```text
Chip       : Apple M1
RAM        : 8 GB
CPU cores  : 8
Free disk  : 11 GB
```

### What that means

| Setup | Fits? |
|---|---|
| Native Ubuntu | ❌ Not viable on Apple Silicon |
| Ubuntu VM | ⚠️ Technically possible, genuinely painful at 8 GB |
| **Docker** | ✅ **Best fit** |
| macOS only | ✅ Fine for Webots/OpenCV, but no ROS 2 |

---

## ⭐ 4. The Recommendation

**Use Docker for ROS 2, and keep using macOS natively for Webots, OpenCV, and
Python.**

Two reasons beyond RAM:

1. **It is what industry does.** NVIDIA ships Isaac ROS as containers. Teams
   deploy robotics software in containers. Learning this way teaches the real
   workflow, not a beginner's shortcut.
2. **It transfers to the Jetson unchanged.** The Jetson Orin Nano runs Ubuntu
   and Docker. The container you build on your Mac runs there too:

```text
MacBook (Docker) ──── same container ────> Jetson Orin Nano ──> Robot
```

A VM teaches you a setup you will then abandon. Docker teaches you the one you
will keep.

### The honest catch

Graphical ROS 2 tools (RViz, Gazebo) are awkward from a container on macOS —
they need X11 forwarding, and performance is poor. **This is fine for us**,
because we already use **Webots on macOS natively** for simulation, and Webots
has its own ROS 2 bridge. Command-line ROS 2 — nodes, topics, publishers,
subscribers, which is what you are learning — works well in Docker.

---

## 🚀 5. Practical — When You Are Ready

```bash
# once Docker Desktop (Apple Silicon build) is installed
docker pull ros:jazzy
docker run -it ros:jazzy bash
```

Inside the container:

```bash
source /opt/ros/jazzy/setup.bash
ros2 --help
ros2 run demo_nodes_cpp talker      # in one terminal
ros2 run demo_nodes_cpp listener    # in another
```

You will see two nodes talking over a topic — the thing Lesson 17 described.

> **⚠️ Status:** Docker is **not installed on this machine yet**, and a
> ~2.5 GB download on the connection we have seen is slow. Lesson 22 therefore
> teaches the real ROS 2 API in a way that runs **without** any installation,
> so you are not blocked.

---

## ⚠️ 6. Common Mistakes

- **Installing a VM with 2 GB RAM** because 4 GB felt like too much — it will
  swap constantly and you will blame ROS 2.
- **Pulling an x86 image on Apple Silicon** — it runs under emulation and feels
  broken. Look for `arm64` images, or expect the slowdown.
- **Trying to build ROS 2 from source on macOS** as a beginner. It can take
  hours and often fails.
- **Believing you must choose one setup forever.** You will use several.

---

## 🎯 7. Interview Question

**Why do robotics teams run ROS 2 in containers?**

> For reproducibility and deployment. A container pins the exact ROS
> distribution and dependencies, so the software behaves identically on a
> developer laptop, in CI, and on the robot's onboard computer.

---

## 🚀 Next — Lesson 22: Your First ROS 2 Program

Nodes, topics, publishers, and subscribers in real ROS 2 Python code — written
so it runs on your Mac today and stays valid when you move into a container.
