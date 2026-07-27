"""
AI Robotics Bootcamp - Lesson 40
QR codes and barcodes: how warehouse robots identify products and shelves.

OCR reads text a human wrote and often guesses. A QR code or barcode carries
data a machine wrote - it decodes exactly, or not at all. Where you control
the labels, a code beats printed text.

Reader:
  - pyzbar (preferred) reads BOTH QR codes and 1-D barcodes reliably.
  - If pyzbar is not installed, we fall back to OpenCV's built-in QR
    detector - which reads QR codes but NOT barcodes.

Install pyzbar (needed for barcodes):
    brew install zbar          # the system library pyzbar wraps
    pip install pyzbar

Usage:
    python qr_reader.py --test              generate codes and read them back
    python qr_reader.py --make SHELF-A204   save a QR code as a PNG
    python qr_reader.py --image f.jpg       read codes in an image
    python qr_reader.py                     live camera
"""

import sys

try:
    import cv2
    import numpy as np
except ImportError:
    print("OpenCV missing.  pip install 'opencv-python<5'")
    sys.exit(1)

# pyzbar is optional. If missing, QR still works via OpenCV; barcodes do not.
try:
    from pyzbar.pyzbar import decode as zbar_decode
    HAVE_PYZBAR = True
except ImportError:
    HAVE_PYZBAR = False


def make_qr(text, size=400, border=40):
    """Create a QR code image containing `text` (for printing labels)."""
    if not hasattr(cv2, "QRCodeEncoder"):
        print("This OpenCV build has no QRCodeEncoder (decoding still works).")
        return None

    encoder = cv2.QRCodeEncoder.create()
    code = encoder.encode(text)
    code = cv2.resize(code, (size, size), interpolation=cv2.INTER_NEAREST)

    # A quiet border is part of the QR spec - without it, readers fail.
    canvas = np.full((size + border * 2, size + border * 2), 255, dtype=np.uint8)
    canvas[border:border + size, border:border + size] = code
    return canvas


def read_codes(image):
    """Find every QR code and barcode in an image.

    Returns a list of (text, kind, corner_points).
    'kind' is e.g. 'QRCODE' or 'EAN13'.
    """
    if HAVE_PYZBAR:
        found = []
        for obj in zbar_decode(image):
            text = obj.data.decode("utf-8", errors="replace")
            pts = np.array([(p.x, p.y) for p in obj.polygon], dtype=int)
            found.append((text, obj.type, pts))
        return found

    # --- Fallback: OpenCV QR only (no barcodes) ---
    detector = cv2.QRCodeDetector()
    try:
        ok, decoded, points, _ = detector.detectAndDecodeMulti(image)
    except cv2.error:
        # OpenCV 4.13 raises a kmeans assertion on very dark frames.
        return []
    if not ok or points is None:
        return []
    return [(t, "QRCODE", np.array(p, dtype=int))
            for t, p in zip(decoded, points) if t]


def annotate(image, codes, colour=(0, 255, 0)):
    """Draw each code's outline and its decoded value."""
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for text, kind, pts in codes:
        poly = np.array(pts).astype(int).reshape(-1, 2)
        cv2.polylines(image, [poly], True, colour, 3)
        x, y = poly[0]
        cv2.putText(image, f"{text} [{kind}]", (int(x), max(int(y) - 10, 16)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2)
    return image


def robot_decision(codes):
    """Turn a decoded code into an action. The code is not the goal - the
    decision is."""
    if not codes:
        return "no code visible -> keep searching"

    text, kind = codes[0][0], codes[0][1]

    if text.upper().startswith("SHELF-"):
        return f"shelf {text[6:]} identified -> navigate to it"
    if text.upper().startswith("DOCK"):
        return "charging dock found -> align and dock"
    if text.upper().startswith("ROOM-"):
        return f"room {text[5:]} identified -> deliver here"
    if text.startswith("http"):
        return "URL found -> fetch item details"
    if kind and kind != "QRCODE":
        return f"barcode {text} ({kind}) -> look the product up in inventory"
    return f"code '{text}' read -> look it up in the database"


def self_test():
    print("=" * 60)
    print("  QR / barcode self-test")
    print("=" * 60)
    print(f"  OpenCV {cv2.__version__}")
    print(f"  pyzbar available : {HAVE_PYZBAR}"
          + ("" if HAVE_PYZBAR else "  (barcodes need: brew install zbar && pip install pyzbar)"))

    samples = ["SHELF-A204", "ROOM-101", "DOCK-1", "https://example.com/item/42"]
    print("\n  QR codes - encode, then read back:\n")
    passed = 0
    for text in samples:
        img = make_qr(text, size=300)
        if img is None:
            break
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        codes = read_codes(img)
        got = codes[0][0] if codes else "(nothing)"
        ok = got == text
        passed += ok
        print(f"    {'OK ' if ok else 'FAIL'}  {text!r:32} -> {got!r}")
    print(f"\n  {passed}/{len(samples)} QR round trips exact")

    # Barcodes need pyzbar. OpenCV's built-in detector does NOT decode them
    # reliably - this was verified, and is why pyzbar is preferred.
    print("\n  Barcodes:")
    if HAVE_PYZBAR:
        print("    pyzbar reads EAN-13, UPC, Code128 etc. from real barcode")
        print("    images and the camera. (No barcode is generated here -")
        print("    point the camera at any product to try it.)")
    else:
        print("    pyzbar not installed - barcode reading unavailable.")
        print("    brew install zbar && pip install pyzbar")

    # Measured robustness of QR decoding.
    print("\n  QR robustness, measured:\n")
    base = cv2.cvtColor(make_qr("SHELF-A204", size=300), cv2.COLOR_GRAY2BGR)

    def works(img):
        return bool(read_codes(img))

    angles = [a for a in (15, 30, 45)
              if works(cv2.warpAffine(base,
                        cv2.getRotationMatrix2D((190, 190), a, 1.0),
                        (380, 380), borderValue=(255, 255, 255)))]
    print(f"    rotation   : readable at {angles} degrees")

    blurs = [k for k in (5, 9, 15) if works(cv2.GaussianBlur(base, (k, k), 0))]
    print(f"    blur       : readable with kernel {blurs}")

    lights = [b for b in (0.5, 0.25, 0.12)
              if works(np.clip(base * b, 0, 255).astype(np.uint8))]
    print(f"    low light  : readable down to {min(lights):.0%} brightness"
          if lights else "    low light  : struggled")

    print("\n  QR reads at an angle, blurred and in dim light - conditions")
    print("  that defeat OCR. That is why warehouses use codes, not text.")

    demo = annotate(base.copy(), read_codes(base))
    cv2.imwrite("output_qr.png", demo)
    print("\n  annotated -> output_qr.png")
    return 0


def make_and_save(text):
    img = make_qr(text)
    if img is None:
        return 1
    name = f"qr_{text.replace('/', '_').replace(':', '')[:30]}.png"
    cv2.imwrite(name, img)
    print(f"Saved {name}  (contains {text!r})")
    print("Print it, stick it on a shelf, and point the robot at it.")
    return 0


def run_image(path):
    image = cv2.imread(path)
    if image is None:
        print(f"Could not read '{path}'")
        return 1

    codes = read_codes(image)
    print(f"\n{path}: {len(codes)} code(s)")
    for text, kind, _ in codes:
        print(f"    [{kind}]  {text!r}")

    cv2.imwrite("output_qr.png", annotate(image.copy(), codes))
    print("\n  annotated -> output_qr.png")
    print(f"  Robot decision: {robot_decision(codes)}")
    return 0


def open_camera(width=1280, height=720):
    # Code reading needs detail - a small code at 640x480 is mush.
    for index in (0, 1, 2):
        cam = cv2.VideoCapture(index)
        if cam.isOpened():
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            ok, frame = cam.read()
            if ok and frame is not None:
                print(f"Camera {index}: {frame.shape[1]}x{frame.shape[0]}")
                return cam
            cam.release()
        if index == 0:
            break
    print("\nNo camera frames. macOS grants camera permission PER APP - run")
    print("this from the terminal inside VS Code, or enable your terminal in")
    print("System Settings > Privacy & Security > Camera, then fully quit it")
    print("(Cmd+Q) and reopen.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())
    if "--make" in sys.argv:
        i = sys.argv.index("--make")
        if i + 1 >= len(sys.argv):
            print("Usage: python qr_reader.py --make SHELF-A204")
            sys.exit(1)
        sys.exit(make_and_save(sys.argv[i + 1]))
    if "--image" in sys.argv:
        i = sys.argv.index("--image")
        if i + 1 >= len(sys.argv):
            print("Usage: python qr_reader.py --image photo.jpg")
            sys.exit(1)
        sys.exit(run_image(sys.argv[i + 1]))

    if not HAVE_PYZBAR:
        print("Note: pyzbar not installed, so only QR codes will read, not")
        print("barcodes.  brew install zbar && pip install pyzbar\n")

    cam = open_camera()
    if cam is None:
        sys.exit(1)

    print("\n  Hold a QR code or barcode up to the camera. Press Q to quit.\n")
    last, misses = None, 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        # Fast enough to run on every frame (unlike OCR).
        codes = read_codes(frame)
        display = annotate(frame, codes)

        decision = robot_decision(codes)
        cv2.rectangle(display, (0, 0), (display.shape[1], 42), (0, 0, 0), -1)
        cv2.putText(display, decision, (12, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0) if codes else (140, 140, 140), 2)

        if decision != last:
            print(f"  {decision}")
            last = decision

        cv2.imshow("QR / Barcode Reader", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
