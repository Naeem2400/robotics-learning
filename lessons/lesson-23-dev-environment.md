# Lesson 23 — Professional Development Environment Setup

**Project 1 — MoveBot**

> **Goal:** set up a development environment to industry standards.

---

## 📌 2026 Reality Check — The Tools That Matter

| Category | Tool | Status |
|---|---|---|
| Programming | Python | ⭐ Essential |
| IDE | VS Code | ⭐ Essential |
| Version control | Git + GitHub | ⭐ Essential |
| AI vision | OpenCV | ⭐ Essential |
| AI models | Ultralytics YOLO | ⭐ Essential |
| Robotics | ROS 2 | ⭐ Essential |
| Simulator | Webots | ⭐ Beginner friendly |
| Advanced simulator | NVIDIA Isaac Sim | ⭐ Professional |
| Containers | Docker | ⭐ Essential |
| AI framework | PyTorch | ⭐ Essential |

---

## 🗂️ Step 1 — Folder Structure

Create one main folder on your Mac:

```text
AI-Robotics-Engineer/
├── 01_Python/
├── 02_OpenCV/
├── 03_YOLO/
├── 04_ROS2/
├── 05_Webots/
├── 06_Projects/
├── 07_Datasets/
├── 08_Docs/
├── requirements/
├── README.md
└── .gitignore
```

This structure will keep 100+ projects organised.

### And a structure for each individual project

```text
MoveBot/
├── README.md          what it does and how to run it
├── .gitignore         keeps secrets and junk out of Git
├── requirements.txt   reproducible dependencies
├── src/               source code
├── tests/             tests
├── docs/              notes and diagrams
├── data/              datasets (not committed)
├── notebooks/         experiments
└── assets/            images, models
```

---

## 🔬 Step 2 — Practical: Scaffold It Automatically

Instead of creating this by hand every time:

```bash
bash new_project.sh MoveBot
bash new_project.sh MoveBot ~/AI-Robotics-Engineer/06_Projects
```

[`new_project.sh`](../new_project.sh) creates the whole structure, a README
template, a `.gitignore`, a `requirements.txt`, and a starter `src/main.py`
that already runs. It refuses to overwrite an existing folder, so it cannot
destroy your work.

> **A detail worth knowing:** the script places a `.gitkeep` file in each empty
> folder. **Git tracks files, not folders** — without that trick, your empty
> `tests/` and `docs/` folders would silently vanish for anyone who clones the
> repository.

---

## 🧩 Step 3 — VS Code Extensions

| Extension | Purpose |
|---|---|
| Python | Official Python support |
| Pylance | Better autocomplete |
| GitHub Pull Requests | GitHub integration |
| Docker | Container management |
| YAML | ROS 2 configuration files |
| Markdown All in One | Professional READMEs |
| Error Lens | Highlights errors inline, instantly |

### What is already installed on this machine

Checked with `code --list-extensions`:

| Extension | Status |
|---|---|
| Python | ✅ installed |
| Pylance | ✅ installed |
| Jupyter | ✅ installed |
| GitHub Pull Requests | ❌ missing |
| Docker | ❌ missing |
| YAML | ❌ missing |
| Markdown All in One | ❌ missing |
| Error Lens | ❌ missing |

Install the missing ones in one command:

```bash
code --install-extension github.vscode-pull-request-github \
     --install-extension ms-azuretools.vscode-docker \
     --install-extension redhat.vscode-yaml \
     --install-extension yzhang.markdown-all-in-one \
     --install-extension usernamehw.errorlens
```

> Of these, **Error Lens** gives beginners the most benefit — it shows the error
> message on the line itself instead of hiding it in a panel you forget to open.

---

## 🐍 Step 4 — Virtual Environment

Every project gets its own environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`.

### ⚠️ Choose your Python version deliberately

On this machine, plain `python3` is version **3.14** — too new for OpenCV,
which has no prebuilt package for it. Use 3.13 instead:

```bash
python3.13 -m venv .venv
```

This is a real lesson from Lesson 14, not a hypothetical: the newest version is
often not the usable one.

---

## 📦 Step 5 — Install Packages

```bash
pip install numpy matplotlib opencv-python ultralytics jupyter
pip list
```

### `requirements.txt`

```text
numpy
opencv-python
matplotlib
ultralytics
jupyter
```

Then anyone — including future you — installs everything with:

```bash
pip install -r requirements.txt
```

> **Pin your versions for real projects:** `numpy==2.1.0` rather than `numpy`.
> Unpinned dependencies are one of the most common causes of "it worked last
> month." Robotics stacks are especially sensitive to this.

---

## 📝 Step 6 — README.md

Every project needs one:

```markdown
# MoveBot

## Objective
Learn robotics simulation using Webots.

## Skills
- Python
- Webots
- Git
- VS Code

## Future
- ROS 2
- AI Vision
```

---

## 🚫 Step 7 — .gitignore

```text
venv/
__pycache__/
.ipynb_checkpoints/
.DS_Store
.env
```

macOS creates `.DS_Store` files automatically — never upload them.

---

## 🧠 Engineering Mindset

| ❌ Beginner | ✅ Professional |
|---|---|
| `Downloads/robot.py`, `test.py`, `new.py`, `new2.py` | `AI-Robotics/Projects/`, `Documentation/`, `Simulation/`, `Testing/` |

### Documentation is part of the job

A professional engineer does not only write code. Good documentation means
another engineer can understand the project, a client can set it up, and
**you** can still understand it in six months.

---

## 🏭 Real Company Workflow

```text
Developer → VS Code → Git commit → GitHub → Code review
   → Simulation → Robot testing → Deployment
```

### The full stack

```text
Python → OpenCV → YOLO → ROS 2 → Webots → Docker → Jetson → Real robot
```

Each layer depends on the one below it.

---

## 💡 2026 Industry Insight

A fast-growing trend in AI robotics:

```text
Robot → Vision AI → LLM → Agent → Robot action
```

Future robots will not only be *programmed* — they will **reason**.

> **User:** "Go to the kitchen and bring my red mug."
>
> **Robot:** locates the kitchen → detects the red mug with its camera →
> plans a path → picks it up → brings it back.

That is not just robotics. It is **AI + Robotics + Agentic AI**.

---

## 🧪 Mini Exercise

Create a GitHub repository and upload a README, a `.gitignore`, and your folder
structure — your first portfolio repository.

> **You already have one.** This course's repository —
> **github.com/Naeem2400/robotics-learning** — has 17 commits, a README,
> a `.gitignore`, and every lesson's code. Rather than starting a second
> repository and splitting your portfolio in two, keep building this one. One
> repository with a long, consistent history is far more convincing to an
> employer than two half-finished ones.

---

## 🚀 Next — Lesson 24: Building MoveBot

We start building: the Webots interface, creating a robot, controlling wheels,
driving forward, turning left and right, speed control, and your first
professional robotics code.

> **Note:** we already built a working Webots robot in Lesson 9
> ([`worlds/first_robot.wbt`](../worlds/first_robot.wbt)), which drives forward,
> stops, and turns. MoveBot can build on that rather than starting over.
