# Lesson 39 — OCR (Optical Character Recognition)

**Module 17 — AI Vision**

> The robot can see objects, faces, poses and gestures. But if a sign says
> **EXIT**, or a box says **Room 204**, or a label says **Paracetamol 500mg** —
> it needs to **read**.

---

## 🎯 Lesson Goal

- What OCR is
- The OCR pipeline
- EasyOCR, PaddleOCR, Tesseract
- Printed vs handwritten text
- OCR in robotics

---

## 📖 The Idea

A warehouse robot needs shelf `A-204`. It photographs the shelf, OCR reads the
label, and the robot drives to the right place.

### Definition

OCR converts text **inside an image** into machine-readable text.

```text
Camera → Image → Preprocessing → OCR → Extracted text → Robot decision
```

### OCR vs Object Detection

| | Answers | Example |
|---|---|---|
| **Object detection** | *What is this?* | `bottle` |
| **OCR** | *What does it say?* | `Water` |

They are complementary, and combining them is a standard industrial workflow:

```text
Camera → YOLO → "bottle" → crop the bottle → OCR → "Coca-Cola" → decision
```

Cropping first matters: OCR on a full frame wastes time reading everything;
OCR on a **detected region** is faster and far more accurate.

---

## 🔬 Practical — Run It

```bash
source .venv/bin/activate

python ocr_reader.py --test           # generates a sign and reads it
python ocr_reader.py --image f.jpg    # read an image file
python ocr_reader.py                  # live camera, press R to read
```

[`ocr_reader.py`](../ocr_reader.py) draws a box around each text region with
its confidence, and — importantly — turns the text into a **decision**.

### Verified output

```text
  Reading a generated sign that says:
    EXIT / Room 204 / Paracetamol 500mg / Battery 12V

  6 text region(s):
      99%  'EXIT'
     100%  'Room'
      92%  '204'
      69%  'Paracetamol 500mg'
     100%  'Battery'
      45%  '12v'

  took 1.02s
  Robot decision: EXIT sign found -> route to the exit
```

**Read those confidences carefully — they are the lesson.**

- `EXIT` and `Battery` scored 99–100%: short, large, high-contrast words.
- `Paracetamol 500mg` scored only **69%** — longer text, smaller glyphs.
- `12V` came back as `'12v'` at **45%**, with the case wrong.

Now recall the medicine example. A system that acts on a 45% read, or that
cannot reliably distinguish case and digits, **must not be trusted to dispense
drugs**. Notice also that OCR split "Room 204" into two separate regions — your
code has to reassemble it. Raw OCR output is messier than tutorials suggest,
and handling that mess *is* the engineering.

### Installation — the pin, again

```bash
pip install easyocr "opencv-python-headless<5"
```

> ⚠️ **Sixth version conflict in this course.** EasyOCR pulls in
> `opencv-python-headless`, and the default is **version 5** — which removes
> `CascadeClassifier` and breaks Lesson 32. The `<5` keeps it at 4.13,
> matching the rest of the project.
>
> The pattern is now unmistakable: **every** library that touches OpenCV tries
> to drag in version 5. This is exactly what `requirements.txt` pins exist for.

The first run downloads ~100 MB of models into `~/.EasyOCR`, then works
offline.

---

## 🧠 The Part That Makes It Robotics

Most OCR tutorials stop at printing text. A robot cannot act on a string — it
needs a **decision**:

```python
if "exit" in text.lower():
    return "EXIT sign found -> route to the exit"
if word.startswith("room"):
    return "Room number read -> navigate to that room"
if "mg" in text.lower():
    return "Medicine label read -> verify against the prescription"
```

That mapping from *text* to *action* is the entire difference between an OCR
demo and an OCR **application**.

---

## ⚙️ Preprocessing — Where Accuracy Actually Comes From

OCR accuracy depends far more on **image quality** than on which library you
pick:

```text
Original → resize → grayscale → denoise → sharpen/threshold → OCR
```

| Problem | Effect | Fix |
|---|---|---|
| Poor lighting | Low accuracy | More light; adaptive threshold |
| Blur | Low accuracy | Steadier camera, faster shutter |
| Tilted text | Missed entirely | Rotate/deskew first |
| Tiny text | Not detected | **Higher resolution**, or move closer |

> **Note the camera setting in the script:** it opens at **1280×720**, not the
> 640×480 used everywhere else in this course. Small text simply vanishes at
> low resolution. This is the one task where you *should* spend the pixels —
> the opposite of the advice in Lesson 31, and knowing when to break the rule
> is the skill.

---

## 📚 The Three Libraries

| Library | Strengths | Trade-offs |
|---|---|---|
| **EasyOCR** | Simple Python API, good accuracy, 80+ languages | Heavier; needs PyTorch |
| **PaddleOCR** | Very accurate and fast, strong on documents | Pulls in PaddlePaddle |
| **Tesseract** | Oldest, lightweight, no Python ML stack | Weaker on photos, needs clean input |

We use **EasyOCR** because PyTorch is already installed from Lesson 35, so it
adds relatively little.

### Printed vs handwritten

All three handle **printed** text well. **Handwriting** is a much harder
problem and generally needs a specialised model — do not expect a general OCR
engine to read a doctor's note.

---

## 🌍 Robotics Applications

| Robot | Reads | To |
|---|---|---|
| Hospital robot | Medicine label | Deliver the right drug |
| Delivery robot | Room number | Find the destination |
| Warehouse robot | Shelf/package label | Pick the right item |
| Agriculture robot | Fertiliser bag | Identify the product |
| Self-checkout | Product name | Price the item |

⚠️ **Safety note:** in the medicine case, OCR confidence must be treated
seriously. A robot that mis-reads `50mg` as `500mg` is dangerous. Real systems
cross-check against a database and refuse to act below a confidence threshold —
they never trust a single read.

---

## 🎯 Interview Question

**Q: Difference between OCR and object detection?**

> Object detection identifies objects in an image. OCR reads text inside the
> image. Combining them lets a robot both recognise an object and read what is
> written on it.

<details>
<summary>Q: Why run object detection before OCR instead of OCR alone?</summary>

Speed and accuracy. OCR across a whole frame processes large empty regions and
picks up irrelevant text — a poster in the background, a label on another
shelf. Detecting the object first gives a small, relevant crop, so OCR runs on
far fewer pixels and returns only text belonging to the object of interest. In
production this can be the difference between 4 fps and 30 fps.
</details>

---

## 🧠 Mini Challenge

A robot sees a bottle labelled **"Water"**.

| | Says |
|---|---|
| YOLO | `bottle` |
| OCR | `Water` |

Together: *"a bottle of water"* — which is enough to decide whether to pick it
up.

---

## 💡 2026 Industry Trend

```text
RGB camera → YOLO → text region detection → OCR
   → Vision-Language Model → natural language understanding → robot action
```

OCR is increasingly combined with **AI reasoning** rather than used for plain
extraction.

---

## 🎥 Reel Idea

**"Can Robots Read Text? 🤖📖"** — point the camera at a book cover, press R,
and let the extracted text appear on screen. The moment the words jump from the
page into the terminal is the shot.

---

## 🏆 Portfolio Projects

**AI OCR Reader** — webcam OCR, image OCR, save and search extracted text.

**Smart Medicine Reader** (stronger):

```text
Medicine box → YOLO detects it → OCR reads the name
   → LLM explains the dosage → voice output → robot speaks
```

This is a genuinely compelling healthcare portfolio piece — but build in the
confidence check above, and say so in the README. Showing that you thought
about failure is what separates a student project from an engineering one.

---

## 🚀 Next — Lesson 40: QR Codes & Barcodes

Detection, inventory robots, warehouse automation, product tracking, smart
checkout, and QR-based navigation.

> **A preview worth knowing:** QR and barcode reading is built into OpenCV
> (`cv2.QRCodeDetector`) — **no extra install**, and far faster and more
> reliable than OCR, because the codes carry error correction. Where you can
> choose a QR code over printed text, you should.
