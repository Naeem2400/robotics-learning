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

## 📖 QR Code vs Barcode

| | Barcode | QR code |
|---|---|---|
| Dimensions | **1-D** (vertical lines) | **2-D** (a grid) |
| Data | ~20 digits | thousands of characters |
| Scan angle | orientation matters | any direction |
| Used on | supermarket products | shelves, tickets, robots |

A barcode holds a product *number* you look up in a database. A QR code can
hold the data itself — a URL, a shelf ID, a robot command.

---

## 🔬 Practical — QR Needs Nothing, Barcodes Need pyzbar

QR reading is built into OpenCV. **Barcode reading is not reliable in OpenCV**
— its built-in detector failed on a standard EAN-13 even at 300 dpi (verified).
The proper tool is **pyzbar**, which reads *both* QR codes and barcodes:

```bash
brew install zbar          # the system library pyzbar wraps (macOS)
pip install pyzbar
```

> The script uses pyzbar when present, and falls back to OpenCV's QR-only
> detector when it is not — so QR always works, and barcodes work once pyzbar
> is installed.

```bash
source .venv/bin/activate

python qr_reader.py --test              # generate QR codes and read them back
python qr_reader.py --make SHELF-A204   # save a printable QR code
python qr_reader.py --image photo.jpg   # read codes in an image
python qr_reader.py                     # live camera
```

### Verified output

```text
  QR codes - encode, then read back:
    OK   'SHELF-A204'                  -> 'SHELF-A204'
    OK   'ROOM-101'                    -> 'ROOM-101'
    OK   'DOCK-1'                      -> 'DOCK-1'
    OK   'https://example.com/item/42' -> 'https://example.com/item/42'
  4/4 QR round trips exact
```

And a real supermarket barcode, read from an image:

```text
  /tmp/barcode.png: 1 code(s)
    [EAN13]  '5901234123457'
  Robot decision: barcode 5901234123457 (EAN13)
                  -> look the product up in inventory
```

**Every read was character-for-character exact.** Compare that with the OCR
results from Lesson 39, where `12V` came back as `'12v'` at 45% confidence.
That difference is the whole point of this lesson.

> **A correction worth noting:** an earlier version of this lesson claimed
> OpenCV could read barcodes because `cv2.barcode` exists. Testing proved
> otherwise — the attribute is present but the decoder needs extra
> super-resolution model files and failed on a clean barcode. *Checking that a
> feature exists is not the same as checking that it works.*

---

## 📊 QR vs OCR — Measured, Not Claimed

The script tests robustness directly rather than repeating folklore:

```text
  QR robustness, measured:

    rotation   : readable at [15, 30, 45] degrees
    blur       : readable with kernel [5, 9, 15]
    low light  : readable down to 12% brightness
```

| Condition | QR code | OCR |
|---|---|---|
| Tilted 45° | ✅ exact | ❌ usually fails |
| Heavy blur | ✅ exact | ❌ fails |
| 12% brightness | ✅ exact | ❌ fails |
| Output correctness | ✅ exact or nothing | ⚠️ *probably* right |

### The nuance most tutorials get wrong

People say *"QR codes survive heavy damage thanks to error correction."* When I
tested it, the truth turned out to be **decoder-dependent**: the same damaged
code that OpenCV's reader gave up on, pyzbar decoded fine — and vice versa on
other damage. Neither tolerated as much as the marketing implies.

The reliable, decoder-independent facts are the ones the robustness table
measured: QR codes read cheerfully at an angle, blurred, and in dim light.
Their *damage* tolerance depends on the code's error-correction level (QR codes
come in L/M/Q/H grades, recovering 7% to 30%) and on which decoder you use — so
do not rely on a specific number.

> **The lesson within the lesson:** I originally wrote a confident "protect the
> corners or the code dies" rule based on one decoder's behaviour. A second
> decoder disproved it. **One measurement is an anecdote; a claim needs to hold
> across conditions before you teach it as a rule.**

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

- **Assuming OpenCV reads barcodes.** `cv2.barcode` exists but does not
  reliably decode them without extra model files — use **pyzbar** (which reads
  QR codes too).
- **Reading only one code when several are visible** — a real problem on a
  shelf with many labels. pyzbar returns all of them.
- **Cropping away the quiet zone.**
- **Low camera resolution.** Like OCR, code reading needs detail; the script
  opens at 1280×720.
- **Trusting a robustness number from a single decoder.** Different libraries
  fail on different damage — see the "nuance" section above.

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

Then grab any product with a barcode on it and hold that up — the reader
returns its number and type (`EAN13`, `UPC-A`, …). Try covering parts of each
code with your thumb and see how much it tolerates before giving up. That is
error correction, measured with your own hand.

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
