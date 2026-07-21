# Lesson 20 — Docker (Professional Robotics Development)

**Module 13 — Docker**

---

## 🎯 Lesson Goal

After this lesson you will understand:

- What Docker is
- What a container is
- What an image is
- The difference between Docker and a virtual machine
- Why robotics uses Docker
- The Docker workflow

---

## 📌 1. The Problem

You build a robotics project on your MacBook. Everything works perfectly. You
send it to a client, and they reply:

> ❌ *"It doesn't work on my computer."*

This is the most famous problem in software.

### What Docker says

> *"I will pack the entire environment and send that."*

Not just the code — the Python version, the libraries, OpenCV, ROS 2, every
dependency, all in one package.

### The cooking analogy

**Without Docker** you send a recipe. In the other kitchen the spices are
different, the rice is different, the stove is different — the result changes.

**With Docker** you send the finished dish in a sealed lunch box. Same result
everywhere.

---

## 📖 2. Image vs Container

This distinction confuses everyone at first, so be precise:

| | What it is | Analogy |
|---|---|---|
| **Image** | A blueprint. A file on disk. Does nothing by itself. | The recipe |
| **Container** | A *running* instance of an image | The cooked meal |

```text
Docker Image  →  docker run  →  Container  →  application running
```

One image can start **many** containers, just as one recipe can cook many
meals. This is why "image" and "container" are not interchangeable.

---

## ⚖️ 3. Docker vs Virtual Machine

| Virtual Machine | Docker Container |
|---|---|
| Runs a whole operating system | Only the app and its dependencies |
| Heavy (gigabytes) | Lightweight (megabytes) |
| Slow to start (minutes) | Fast to start (seconds) |
| Lots of RAM | Little RAM |

**A virtual machine is a whole new computer. A container is a new room in the
house you already have.** That is why Docker is so much faster — the room
shares the building's foundations (the kernel) instead of rebuilding them.

---

## 🤖 4. Why Robotics Uses Docker

A robot project might need ROS 2, OpenCV, YOLO, PyTorch, CUDA, and a specific
Python version.

| Approach | Time |
|---|---|
| Installing all of it by hand | 2–3 hours, and it often breaks |
| `docker run ...` | ~2 minutes |

**You have already experienced this problem in this course.** In Lesson 14,
OpenCV could not be installed because the system Python was 3.14 and no
prebuilt package existed for it. A container ships its *own* Python, so that
mismatch simply cannot happen.

### Deployment

```text
MacBook  →  Docker  →  Jetson Orin Nano  →  Robot
```

Same container, same behaviour. This is the real payoff: the thing you tested
on your laptop is the *identical* thing running on the robot.

### Real companies

| Company | Use |
|---|---|
| **NVIDIA** | Ships Isaac ROS as Docker containers |
| **OpenAI** | Deploys AI services in containers |
| **Amazon Robotics** | Warehouse services in containers |
| **Figure AI** | Containerised development |

---

## 💻 5. Practical — The Commands

```bash
docker --version              # check it is installed

docker run hello-world        # the classic first test
```

Expected output:

```text
Hello from Docker!
```

```bash
docker pull python:3.12       # download an image
docker run -it python:3.12    # start a container and go inside it
exit                          # leave the container
```

### The workflow

```text
Write code → build image → run container → test → share → deploy
```

---

### ⚠️ Status on this machine

**Docker is not installed here yet.** Two things to know before you try:

1. **Docker Desktop is a ~2.5 GB download.** This machine currently has about
   11 GB free, so it fits — but on a slow connection it takes a long time.
   Earlier in this course a 55 MB download stalled repeatedly, so plan for a
   good connection.
2. **On Apple Silicon**, install the **Apple Silicon (ARM64)** build of Docker
   Desktop. Some robotics images are built for x86 only and will run slowly
   through emulation, or not at all. When that happens the error mentions
   `platform mismatch` or `linux/amd64` — that is the cause, not your code.

A lighter alternative to Docker Desktop on macOS is **Colima**
(`brew install colima docker`), which runs containers without the Desktop
application and uses less RAM — worth knowing on an 8 GB machine.

---

## ⚠️ 6. Common Mistakes

- **Thinking Docker is a virtual machine.** It is not — it shares the host
  kernel.
- **Confusing an image with a container.** The image is the blueprint; the
  container is the running thing.
- **Putting an entire project in one container.** Professional systems often
  use separate containers for separate services.
- **Forgetting containers are disposable.** Files written inside a container
  disappear when it is deleted, unless you mount a volume. Beginners lose work
  this way.
- **Ignoring architecture (ARM vs x86)** on Apple Silicon.

---

## 🎯 7. Interview Question

**What is the difference between Docker and a virtual machine?**

> A virtual machine runs a complete operating system. A Docker container
> isolates only the application and its dependencies, which makes it much
> lighter and faster.

<details>
<summary>Follow-up: why is a container so much smaller than a VM?</summary>

A container shares the **host's kernel** instead of shipping its own. A VM must
include an entire guest OS — kernel, drivers, system services — before your
application even starts. A container only adds the libraries your app needs on
top of a kernel that is already running, so it starts in seconds rather than
minutes.
</details>

---

## 💡 8. 2026 Industry Note

Modern AI robotics projects commonly use:

Docker · GitHub Actions (CI/CD) · ROS 2 · PyTorch ·
Kubernetes (large deployments) · NVIDIA Container Toolkit (GPU systems)

**Do not learn Kubernetes yet.** Get Docker solid first.

---

## 🧠 Mini Exercise

Your robot uses Python, OpenCV, YOLO, and ROS 2. What is the biggest advantage
of handing this project to another engineer as a Docker container?

> **They get exactly the environment that existed on your MacBook**, so the
> "works on my machine" problem largely disappears.

---

## 🗺️ Roadmap

```text
Python ✅  Linux ✅  Git ✅  Docker ✅  OpenCV ✅  YOLO ✅  ROS 2 basics ✅
        ↓
ROS 2 practical → Webots simulation → Arduino → ESP32 → Jetson
        ↓
LLM integration → Agentic robotics
```

---

## 🚀 Next — Lesson 21: Your First ROS 2 Program

Theory is done. From here we build actual robotics software: workspaces,
packages, nodes, topics, publishers, subscribers, and Webots integration — and
you will watch one ROS 2 node talk to another live.

> **Recommended first:** a short lesson on **Ubuntu VM vs native Ubuntu vs
> Docker vs macOS**, to choose the setup that is realistic on a MacBook Air M1
> with 8 GB of RAM. Picking the right one now means the same workflow carries
> over to a Jetson Orin Nano later, with nothing to relearn.
