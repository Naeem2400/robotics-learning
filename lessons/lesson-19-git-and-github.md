# Lesson 19 — Git & GitHub (Industry Workflow)

**Module 12 — Software Engineering for Robotics**

> Until now we were learning **robotics**. From here we learn **robotics
> engineering**. These are different things.

---

## 📌 The Problem Git Solves

You write code. One day you have 5,000 lines of robot software. The next day a
file is deleted by accident, or a change introduces a bug that breaks
everything.

Do you rewrite it all? 😱

That is why Git exists.

### The thing everyone has done

```text
Thesis_Final.docx
Thesis_Final2.docx
Thesis_Final_Final.docx
Thesis_Final_Last.docx
Thesis_Final_Last_Real.docx
```

With Git, there is one project and a complete history.

---

## 📖 1. What Is Git?

### Technical definition

Git is a **Distributed Version Control System (DVCS)**. It records the history
of your code.

### In plain terms

Git is your project's **time machine**. Every change is recorded, so if
something breaks you can return to any earlier state.

## What Is GitHub?

| | Where it lives | What it gives you |
|---|---|---|
| **Git** | On your laptop | Version history |
| **GitHub** | On the internet | Backup + portfolio + collaboration |

Git works perfectly with no internet. GitHub is where you *share* it.

### Industry

Tesla, Boston Dynamics, NVIDIA, OpenAI, Google — every software company uses
Git. Not most. **Every one.**

---

## 🔄 2. The Workflow

```text
Code → git add → git commit → git push → GitHub
```

| Command | What it means |
|---|---|
| `git init` | Start tracking this folder |
| `git status` | What has changed? |
| `git add file.py` | Stage this file for the next snapshot |
| `git add .` | Stage everything |
| `git commit -m "message"` | **Take a snapshot of this moment** |
| `git log` | Show the history |
| `git push` | Send commits to GitHub |

### The `.git` folder

After `git init`, a hidden folder called `.git` appears. It is Git's brain —
the entire history lives inside it. **Never edit it by hand.**

---

## 🔬 3. Practical — Practise Safely

```bash
bash git_practice.sh
```

[`git_practice.sh`](../git_practice.sh) builds a **throwaway repository** in a
temporary folder, runs the entire workflow, shows the real output of every
step, then deletes it. Your actual project is never touched, so you cannot
break anything.

It walks through: `init` → `status` → `add` → `commit` → change → commit →
`branch` → `merge` → viewing an old commit.

### Reading `git status`

The short form uses single letters:

| Symbol | Meaning |
|---|---|
| `??` | **Untracked** — Git sees the file but is not watching it |
| `A` | **Added** — staged, ready to commit |
| `M` | **Modified** — a tracked file has changed |

---

## 🌿 4. Branches

Suppose one engineer builds voice AI while another builds navigation, both
editing the same files. Conflict.

Branches solve this:

```text
main
├── voice
├── navigation
├── vision
└── testing
```

Each person works in isolation, then the work merges back.

The practice script demonstrates this concretely: it creates a `voice-feature`
branch and adds a commit there, then switches back to `main` and shows that
main **still has the old file, unchanged**. The experiment cannot break the
working version. After `git merge`, the work appears in main.

```text
Feature → Branch → Code → Commit → Push → Pull Request → Merge
```

Every company uses this workflow. In a real robotics project:

```text
Robot
├── Vision team
├── Navigation team
├── AI team
├── Electronics team
└── Cloud team
```

Each team on its own branch.

---

## 🚫 5. `.gitignore`

This file tells Git which files to **never** upload:

```text
venv/
__pycache__/
.env
```

### ⚠️ Never commit secrets

**Never put passwords or API keys on GitHub.** And understand this clearly:
deleting a secret in a later commit does **not** remove it — it stays in the
history forever, and public repositories are scanned by bots within minutes. If
a key is ever committed, the only safe fix is to revoke and regenerate it.

This repository's own `.gitignore` excludes `.venv/`, `__pycache__/`, generated
images, and Webots' temporary files.

---

## 📁 Project Structure

```text
robot_project/
├── robot.py
├── README.md
├── requirements.txt
├── .gitignore
└── venv/            (ignored by Git)
```

---

## 📚 6. Learn From This Repository's Real History

You do not need a toy example. **This course's repository is a real Git
project**, and every lesson was committed as we built it:

```bash
git log --oneline
```

```text
9cb0ab8 Lesson 18: Linux for robotics
ed93d22 Fail gracefully when OpenCV is missing
91f9d0a Lesson 17: ROS 2 - nodes, topics, publishers and subscribers
985caac Lesson 16: YOLO object detection
f4708e6 Lessons 14-15: OpenCV and how a robot sees an image
...
ed0833a Lesson 1: Python for Robotics - variables and decisions
```

See exactly what one commit changed:

```bash
git show --stat 9cb0ab8
```

```text
 README.md                               |   4 +-
 lessons/lesson-18-linux-for-robotics.md | 269 +++++++++++++++++++++
 linux_check.sh                          |  80 ++++++++
 3 files changed, 352 insertions(+), 1 deletion(-)
```

### What good commit messages look like

Notice the pattern in the history above. Each message says **what changed and
why**, not "update" or "fix". Compare:

| ❌ Weak | ✅ Clear |
|---|---|
| `update` | `Lesson 17: ROS 2 - nodes, topics, publishers` |
| `fix bug` | `Fail gracefully when OpenCV is missing` |
| `changes` | `Restructure modules to match lesson content` |

Six months from now, `git log` is the only explanation of *why* the code looks
the way it does. Write for that reader.

---

## ⚠️ 7. Common Mistakes

- **Committing secrets** — see the warning above.
- **Committing `venv/`** — hundreds of megabytes that everyone can regenerate
  from `requirements.txt`.
- **Vague commit messages** — `update` tells nobody anything.
- **One giant commit** — commit small, related changes so you can undo one
  thing without losing everything.
- **Only committing when "finished"** — commit as you go. That is the point.

---

## 🎯 8. Interview Question

**What is the difference between Git and GitHub?**

> Git is the version control tool that runs on your machine. GitHub is an
> online platform for storing Git repositories and collaborating on them.

<details>
<summary>Follow-up: what does "distributed" mean in DVCS?</summary>

Every clone contains the **complete history**, not just the latest version.
You can commit, branch, and inspect the log with no network connection, and if
the server disappears, any developer's copy can restore the whole project.
Older systems kept history only on a central server, which was a single point
of failure.
</details>

---

## 💡 9. 2026 Industry Note

It is not only GitHub — companies also use **GitLab**, **Bitbucket**, and
**Azure DevOps**. The platform changes; the Git concepts underneath are
identical.

### A robotics engineer's daily routine

```text
Pull latest code → write code → run simulation → fix bugs
   → commit → push → review → merge
```

---

## 📈 Progress

```text
Python ✅   Linux ✅   OpenCV ✅   YOLO ✅   ROS 2 basics ✅   Git ✅
```

---

## 🚀 Next — Lesson 20: Docker

The solution to *"but it works on my computer."* Important because ROS 2
projects run in Docker, NVIDIA Isaac ROS uses it, AI models deploy in
containers, and professional teams need reproducible environments.

We will cover what Docker is, containers vs virtual machines, images vs
containers, Docker Desktop on Apple Silicon, and running a first container.
