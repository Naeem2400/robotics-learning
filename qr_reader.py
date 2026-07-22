"""
AI Robotics Bootcamp - Lesson 40
QR codes and barcodes: how warehouse robots really identify things.

OCR reads text a human wrote. QR codes carry data a machine wrote, with
error correction built in. Measured here: they read fine at 45 degrees, under
heavy blur, and at 25% brightness - conditions that defeat OCR - but they
tolerate only mild physical damage. Where you control the labels, a code
beats printed text.

Everything here uses OpenCV only. No extra installation.

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


def make_qr(text, size=400, border=40):
    """Create a QR code image containing `text`.

    Useful for printing your own shelf, room or docking labels.
    """
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
    """Find every QR code in an image.

    Returns a list of (data, corner_points).
    """
    detector = cv2.QRCodeDetector()

    # detectAndDecodeMulti finds SEVERAL codes; the single-code version
    # silently ignores all but one, which bites people in warehouses where
    # a shelf has many labels in view at once.
    try:
        ok, decoded, points, _ = detector.detectAndDecodeMulti(image)
    except cv2.error:
        # OpenCV 4.13 raises a kmeans assertion on very dark or degenerate
        # frames instead of simply reporting "no code". Treat it as none.
        return []
    if not ok or points is None:
        return []

    found = []
    for text, pts in zip(decoded, points):
        if text:                       # a detected but unreadable code gives ""
            found.append((text, pts))
    return found


def read_barcodes(image):
    """Find 1-D barcodes (the striped kind on products)."""
    if not hasattr(cv2, "barcode"):
        return []

    detector = cv2.barcode.BarcodeDetector()
    ok, decoded, types, points = detector.detectAndDecodeWithType(image)
    if not ok or points is None:
        return []

    return [(t, ty, p) for t, ty, p in zip(decoded, types, points) if t]


def annotate(image, codes, colour=(0, 255, 0)):
    """Draw each code's outline and its decoded value."""
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for text, pts in codes:
        poly = np.array(pts).astype(int).reshape(-1, 2)
        cv2.polylines(image, [poly], True, colour, 3)
        x, y = poly[0]
        cv2.putText(image, text, (int(x), max(int(y) - 10, 16)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, colour, 2)
    return image


def robot_decision(codes):
    """Turn a decoded code into an action.

    The point of this lesson: the code is not the goal, the decision is.
    """
    if not codes:
        return "no code visible -> keep searching"

    text = codes[0][0]

    if text.upper().startswith("SHELF-"):
        return f"shelf {text[6:]} identified -> navigate to it"
    if text.upper().startswith("DOCK"):
        return "charging dock found -> align and dock"
    if text.upper().startswith("ROOM-"):
        return f"room {text[5:]} identified -> deliver here"
    if text.startswith("http"):
        return "URL found -> fetch item details"
    return f"code '{text}' read -> look it up in the database"


def self_test():
    print("=" * 58)
    print("  QR code self-test  (no installation required)")
    print("=" * 58)
    print(f"  OpenCV {cv2.__version__}")
    print(f"  QRCodeDetector : {hasattr(cv2, 'QRCodeDetector')}")
    print(f"  QRCodeEncoder  : {hasattr(cv2, 'QRCodeEncoder')}")
    print(f"  Barcode        : {hasattr(cv2, 'barcode')}")

    samples = ["SHELF-A204", "ROOM-101", "DOCK-1", "https://example.com/item/42"]
    print("\n  Encoding, then reading back:\n")

    passed = 0
    for text in samples:
        img = make_qr(text, size=300)
        if img is None:
            break
        codes = read_codes(img)
        got = codes[0][0] if codes else "(nothing)"
        ok = got == text
        passed += ok
        print(f"    {'OK ' if ok else 'FAIL'}  {text!r:32} -> {got!r}")

    print(f"\n  {passed}/{len(samples)} round trips exact\n")

    # Measured robustness. The folklore says "QR codes survive damage";
    # the truth is more specific, and worth knowing.
    print("  Robustness, measured on this OpenCV build:\n")

    base = make_qr("SHELF-A204", size=300)

    def works(img):
        return bool(read_codes(img))

    # Rotation
    angles = [a for a in (15, 30, 45)
              if works(cv2.warpAffine(base,
                        cv2.getRotationMatrix2D((190, 190), a, 1.0),
                        (380, 380), borderValue=255))]
    print(f"    rotation      : readable at {angles} degrees")

    # Blur
    blurs = [k for k in (5, 9, 15) if works(cv2.GaussianBlur(base, (k, k), 0))]
    print(f"    blur          : readable with kernel {blurs}")

    # Low light
    lights = [b for b in (0.5, 0.25, 0.12)
              if works(np.clip(base * b, 0, 255).astype(np.uint8))]
    print(f"    low light     : readable down to {min(lights):.0%} brightness")

    # Damage to the DATA area
    survived = []
    for px in (20, 50, 80):
        d = base.copy()
        d[150:150 + px, 150:150 + px] = 255
        if works(d):
            survived.append(f"{100.0 * px * px / (380 * 380):.1f}%")
    print(f"    data damage   : survives up to {survived[-1] if survived else 'none'}")

    # Damage to a FINDER PATTERN (a corner square)
    d = base.copy()
    d[20:90, 20:90] = 255
    print(f"    corner damage : {'readable' if works(d) else 'UNREADABLE'} "
          f"(finder pattern destroyed)")

    print("\n  So: excellent against angle, blur and dim light - all the")
    print("  things that defeat OCR. But only mild damage tolerance, and")
    print("  destroying a CORNER square kills it outright: error correction")
    print("  protects the data, not the three locator squares.")

    demo = annotate(make_qr("SHELF-A204", size=300),
                    read_codes(make_qr("SHELF-A204", size=300)))
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
    bars = read_barcodes(image)

    print(f"\n{path}:")
    print(f"  QR codes : {len(codes)}")
    for text, _ in codes:
        print(f"    {text!r}")
    print(f"  Barcodes : {len(bars)}")
    for text, kind, _ in bars:
        print(f"    {text!r} ({kind})")

    cv2.imwrite("output_qr.png", annotate(image.copy(), codes))
    print(f"\n  annotated -> output_qr.png")
    print(f"  Robot decision: {robot_decision(codes)}")
    return 0


def open_camera(width=1280, height=720):
    # Like OCR, code reading needs detail - a small QR at 640x480 is mush.
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

    cam = open_camera()
    if cam is None:
        sys.exit(1)

    print("\n  Hold a QR code up to the camera. Press Q to quit.\n")
    last, misses = None, 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        # Unlike OCR, this is fast enough to run on EVERY frame.
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
