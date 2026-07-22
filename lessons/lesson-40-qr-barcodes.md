# Lesson 40 — QR Codes & Barcode Detection

**Module 17 — AI Vision**

> OCR reads text a *human* wrote. A QR code carries data a *machine* wrote —
> and that changes everything about reliability.

---

## 🎯 Lesson Goal

- QR code and barcode detection
- Why warehouses use codes instead of text
- Inventory and product tracking
- Robot navigation using QR markers

---

## 🔬 Practical — Nothing to Install

This is the rare lesson that needs **no new library**. QR encoding, QR
decoding, and barcode reading are all built into the OpenCV you already have:

```bash
source .venv/bin/activate

python qr_reader.py --test              # generate codes and read them back
python qr_reader.py --make SHELF-A204   # save a printable QR code
python qr_reader.py --image photo.jpg   # read codes in an image
python qr_reader.py                     # live camera
```

### Verified output

```text
  OpenCV 4.13.0
  QRCodeDetector : True
  QRCodeEncoder  : True
  Barcode        : True

  Encoding, then reading back:
    OK   'SHELF-A204'                  -> 'SHELF-A204'
    OK   'ROOM-101'                    -> 'ROOM-101'
    OK   'DOCK-1'                      -> 'DOCK-1'
    OK   'https://example.com/item/42' -> 'https://example.com/item/42'

  4/4 round trips exact
```

**Every read was character-for-character exact.** Compare that with the OCR
results from Lesson 39, where `12V` came back as `'12v'` at 45% confidence.
That difference is the whole point of this lesson.

---

## 📊 QR vs OCR — Measured, Not Claimed

The script tests robustness directly rather than repeating folklore:

```text
  Robustness, measured on this OpenCV build:

    rotation      : readable at [15, 30, 45] degrees
    blur          : readable with kernel [5, 9, 15]
    low light     : readable down to 25% brightness
    data damage   : survives up to 1.7%
    corner damage : UNREADABLE (finder pattern destroyed)
```

| Condition | QR code | OCR |
|---|---|---|
| Tilted 45° | ✅ exact | ❌ usually fails |
| Heavy blur | ✅ exact | ❌ fails |
| 25% brightness | ✅ exact | ❌ fails |
| Output correctness | ✅ exact or nothing | ⚠️ *probably* right |

### The nuance most tutorials get wrong

People say *"QR codes have error correction, so they survive damage."* Our
measurements show that is **only half true**:

- Damage to the **data area**: tolerated, but only up to about **1.7%** of the
  image with OpenCV's decoder — far less than the marketing suggests.
- Damage to a **corner square**: **fatal.** Unreadable immediately.

Those three corner squares are **finder patterns** — the decoder uses them to
locate and orient the code. Error correction protects the **data**, not the
locators. A scuffed corner kills a label that a torn middle would survive.

> **Practical consequence:** when you print QR labels for a robot, protect the
> corners. Laminate them, or leave a wide margin. That single piece of
> knowledge prevents a whole class of warehouse failures.

### The most important difference

**OCR guesses. QR either decodes exactly or returns nothing.**

For a medicine-dispensing robot, "nothing" is a *safe* failure — the robot
stops and asks. A 45%-confidence guess at a dosage is a *dangerous* failure.
**Where you control the labels, always choose a code.**

---

## 🏷️ Making Your Own Labels

```bash
python qr_reader.py --make SHELF-A204
```

Saves a printable PNG. Stick it on a shelf and the robot can identify that
location precisely.

> **A spec detail that catches people:** a QR code needs a **quiet zone** — a
> plain white border around it. Crop that off and readers fail, even though the
> code "looks" complete. The script adds one automatically.

---

## 🤖 Code → Decision

As always, decoding is not the goal:

```python
if text.startswith("SHELF-"):  return "navigate to that shelf"
if text.startswith("DOCK"):    return "align and dock for charging"
if text.startswith("ROOM-"):   return "deliver here"
```

| Robot | Code says | Robot does |
|---|---|---|
| Warehouse | `SHELF-A204` | Drive to shelf A204 |
| Delivery | `ROOM-101` | Deliver to room 101 |
| Any mobile robot | `DOCK-1` | Align and charge |
| Inventory | `https://…/item/42` | Look the item up |

### QR codes as navigation markers

This is a genuinely common technique: stick QR codes on floors, walls, or
docking stations. Because the detector returns the code's **four corner
points**, a robot can work out not just *which* marker it sees but **how far
away and at what angle** it is — from the corners' size and shape in the frame.

That is how many warehouse robots localise cheaply, without expensive sensors.
Amazon-style fulfilment centres use exactly this idea with floor markers.

---

## ⚡ One More Advantage: Speed

OCR in Lesson 39 took **~1 second** per read — far too slow for every frame,
which is why `ocr_reader.py` only reads when you press **R**.

QR detection is fast enough to run on **every single frame**, which is why
`qr_reader.py` just does it continuously. For a moving robot, that difference
decides whether the technique is usable at all.

---

## ⚠️ Common Mistakes

- **Using `detectAndDecode` instead of `detectAndDecodeMulti`.** The single
  version silently returns just one code — a real problem on a shelf with
  several labels in view.
- **Cropping away the quiet zone.**
- **Low camera resolution.** Like OCR, code reading needs detail; the script
  opens at 1280×720.
- **Assuming error correction saves damaged corners.** It does not.
- **Not handling the decoder crash.** OpenCV 4.13 raises a `kmeans` assertion
  on very dark frames instead of reporting "no code" — `qr_reader.py` catches
  it. Found by testing at 12% brightness.

---

## 🎯 Interview Questions

**Q: Why do warehouses use QR codes rather than printed text?**

> Because decoding is exact and fast. A QR code either returns the right data
> or none at all, it carries error correction, and it can be read at an angle,
> blurred, or in poor light — conditions where OCR degrades into guesswork.

<details>
<summary>Q: How can a robot estimate distance from a QR code?</summary>

The detector returns the code's four corner points. Since the printed code has
a known physical size, the size and shape of that quadrilateral in the image
give both distance and viewing angle — a bigger square means closer, and a
skewed square means off-axis. This is the same maths as ArUco/AprilTag markers,
which robotics uses specifically for pose estimation.
</details>

---

## 🧠 Mini Challenge

Print a code with `python qr_reader.py --make DOCK-1`, hold it to the camera,
and watch the decision change to *"charging dock found → align and dock"*.

Then **cover one corner square with your thumb.** It stops reading instantly.
Now cover a bit of the middle instead — it keeps working. That is finder
patterns versus error correction, in one experiment.

---

## 🎥 Reel Idea

**"Why Robots Don't Read Text 🤖"** — show OCR struggling with a tilted, dim
label, then a QR code decoding instantly under the same conditions. End on the
thumb-over-the-corner trick.

---

## 🏆 Portfolio Project

**Warehouse Inventory Robot** — a camera reads shelf QR codes, maps them to a
product database, tracks stock, and navigates by marker. Combine with the
Lesson 36 follower and you have a robot that finds a shelf and drives to it.

---

## 🚀 Next

With reading and code-scanning done, the vision module is essentially complete.
The natural next step is putting these capabilities **on a robot** — feeding
detections into ROS 2, and from there into simulation and real hardware.
