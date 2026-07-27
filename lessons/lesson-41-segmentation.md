# Lesson 41 — Image Segmentation (SAM2 & Modern AI Vision)

**Module 17 — AI Vision**

> YOLO draws a **box** around an object. But a robot arm cannot grasp a box —
> it needs the object's **exact shape**. That is segmentation.

---

## 🎯 Lesson Goal

- What image segmentation is
- Semantic vs instance vs panoptic segmentation
- The Segment Anything Model (SAM2)
- Segmentation in robotics: pick-and-place, autonomous vehicles

---

## 📖 The Problem With Boxes

A table has an apple, a cup, and a phone. YOLO gives each a rectangle. Now the
robot wants to pick up the cup — but the rectangle is not the cup's shape. Grasp
at the box centre and the gripper may close on empty air or the wrong edge.

### Definition

Segmentation classifies **every pixel** of an image — so instead of a box, you
get the object's exact outline (a *mask*).

---

## 🔬 Practical — Box vs Mask, Measured

```bash
source .venv/bin/activate

python segmentation.py --test           # sample image, no camera
python segmentation.py --image f.jpg    # your own image
python segmentation.py                  # live camera
```

[`segmentation.py`](../segmentation.py) uses YOLO's **`-seg`** model, which
outputs masks and needs **no new install**. Verified output:

```text
  4 object(s):
    bus        box=  402091px  mask=  262639px  fill= 65%  grasp=(438,442)
    person     box=   67574px  mask=   21927px  fill= 32%  grasp=(767,667)
    person     box=   96965px  mask=   50455px  fill= 52%  grasp=(281,621)
    person     box=   56194px  mask=   35106px  fill= 62%  grasp=(281,621)

  On average, only 53% of each bounding box is actually the object.
```

**Stop on that `fill` column — it is the entire lesson.**

- The bus box is 65% bus, 35% background.
- One person's box is only **32% the person** — two thirds of it is street,
  bus, and other people.

A robot arm told to grasp at the **centre of the box** would, for that person,
close on empty pavement. The `grasp` column is the **centroid of the mask** —
always a point that is genuinely on the object. The script draws it as a yellow
cross, and you can see each cross sits on the object, never on background.

> **This is why detection is not enough for manipulation.** Navigation and
> counting only need a rough location, so a box is fine. Grasping needs the
> shape.

---

## 🧩 The Three Kinds of Segmentation

| Type | What it separates | Example |
|---|---|---|
| **Semantic** | Every pixel by **class** | all "car" pixels one colour — but two cars merge |
| **Instance** | Each **object** individually | Car 1, Car 2, Car 3 — separate masks |
| **Panoptic** | Semantic **+** instance | every object *and* the background labelled |

**Instance segmentation is the one robotics usually wants** — a robot picking
boxes needs to know that *this* box is separate from the one behind it. YOLO's
`-seg` model does instance segmentation, which is why the demo gives each person
its own mask.

---

## 🤖 SAM2 — Segment Anything

**SAM2** (Segment Anything Model 2, from Meta AI) is the state of the art. You
click any object in an image — even one the model has never seen — and it
returns a precise mask.

| | YOLO-seg | SAM2 |
|---|---|---|
| Knows object *classes* | ✅ (80 COCO classes) | ❌ (segments anything, names nothing) |
| Segments unknown objects | ❌ | ✅ |
| Runs on a laptop CPU | ✅ | heavy — wants a GPU |
| Install size | ~6 MB | hundreds of MB |

They are complementary: **YOLO says *what* it is; SAM2 says *exactly where* it
is.** A common modern pipeline uses YOLO to name and locate, then SAM2 to get a
clean mask for grasping.

> This course uses YOLO-seg for the practical because it runs on your machine
> today. The concepts — masks, instances, grasp points — transfer to SAM2
> unchanged.

---

## 🏗️ The Robotics Pipeline

```text
RGB camera → YOLO (what & where) → SAM2 / seg (exact mask)
   → depth camera (how far) → grasp planning → robot arm
```

### Why a depth camera too?

A mask is 2-D — it gives the object's shape *in the image*, but not how far
away it is. A robot arm reaching for a cup needs the distance:

```text
cup mask → cup centroid at (438, 442) → depth camera → 42 cm away → reach
```

Depth sensors (Intel RealSense, Luxonis OAK-D) supply that third dimension.
We will use them later.

### Applications

| Robot | Segments | To |
|---|---|---|
| Warehouse | a box | grasp it precisely |
| Agriculture | a fruit | pick without crushing |
| Surgical | an organ | operate safely |
| Self-driving | road, lane, pedestrian | drive safely |

---

## ⚠️ Common Mistakes

- **Treating detection and segmentation as the same.** A box is a location; a
  mask is a shape.
- **Grasping at the box centre.** As measured above, that centre is often not
  on the object.
- **Thinking segmentation is only for medical imaging.** It is central to
  industrial pick-and-place.
- **Assuming you always need SAM2.** For known object classes, YOLO-seg is
  smaller, faster, and enough.

---

## 🎯 Interview Questions

**Q: Why does a robot arm use segmentation rather than detection?**

> A robot arm needs the object's exact boundary to choose a valid grasp point.
> A bounding box includes background pixels, so grasping from the box centre can
> miss the object entirely.

<details>
<summary>Q: Semantic vs instance segmentation — which for a bin-picking robot?</summary>

Instance segmentation. A bin of identical parts is the worst case for semantic
segmentation, which would merge all the parts into one "part" blob. The robot
must know where one item ends and the next begins to pick a single object, and
only instance segmentation gives each its own mask.
</details>

---

## 🧠 Mini Challenge

A table has two apples and a cup.

- **Detection** returns: `apple`, `apple`, `cup`.
- **Instance segmentation** returns: `apple #1`, `apple #2`, `cup #1` — each
  with its own pixel mask.

Run `segmentation.py` with two of the same object in frame and confirm each
gets its own coloured mask and its own grasp cross.

---

## 🎥 Reel Idea

**"Why Robots Need More Than YOLO"** — show the YOLO box, then the segmentation
mask over the same object, then the number: *"only 32% of that box is the
object."* End on the grasp cross snapping onto the object's true centre.

---

## 🏆 Portfolio Project

**AI Object Segmentation System** — segment objects, visualise masks, compute
grasp points, and show the box-fill percentage side by side with YOLO. The
grasp-point analysis makes it read as *robotics*, not just a vision demo.

---

## 📚 Homework — Know These Names

Research the purpose of each; we use them in later projects:

1. **SAM2** (Segment Anything Model 2)
2. **Depth Anything V2**
3. **Intel RealSense D455**
4. **Luxonis OAK-D**
5. **YOLO segmentation models**

---

## 🚀 Next — Lesson 42: Multi-Object Tracking (MOT)

Not just detecting objects, but giving each a **persistent ID** and following it
across every frame — `Person #1`, `Person #2`, `Dog #3`. We already saw the
foundation in Lesson 36; MOT scales it to many objects at once, as used in
airport surveillance, smart factories, and warehouse robots.
