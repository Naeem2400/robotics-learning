"""
AI Robotics Bootcamp - Lesson 39
OCR: teaching the robot to read.

Object detection tells the robot "that is a bottle".
OCR tells it the bottle says "Water".

    camera/image -> preprocessing -> OCR -> text -> robot decision

Usage:
    python ocr_reader.py --test           generate a test image and read it
    python ocr_reader.py --image f.jpg    read text in an image file
    python ocr_reader.py                  live camera, press R to read
"""

import sys
import time

try:
    import cv2
    import numpy as np
except ImportError:
    print("OpenCV missing.  pip install 'opencv-python<5'")
    sys.exit(1)

LANGS = ["en"]
MIN_CONFIDENCE = 0.4


def load_reader():
    """Create the EasyOCR reader.

    The first run downloads detection and recognition models (~100 MB) and
    caches them in ~/.EasyOCR, so it is slow once and fast afterwards.
    """
    try:
        import easyocr
    except ImportError:
        print("EasyOCR is not installed. Install it WITH the pin:\n")
        print('    pip install easyocr "opencv-python-headless<5"\n')
        print("The pin matters: EasyOCR pulls opencv-python-headless, and the")
        print("default is version 5, which removes CascadeClassifier and")
        print("breaks the face detection from Lesson 32.")
        sys.exit(1)

    print("Loading OCR models (first run downloads ~100 MB) ...")
    return easyocr.Reader(LANGS, gpu=False, verbose=False)


def preprocess(image):
    """Clean an image up before reading it.

    OCR accuracy depends far more on image quality than on the library.
    Grayscale removes colour noise, and the threshold turns faint text into
    solid black on white, which is what the recogniser expects.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)      # denoise, keep edges sharp
    return gray


def read_text(reader, image, show_preprocessing=False):
    """Run OCR and return a list of (text, confidence, box)."""
    source = preprocess(image) if show_preprocessing else image
    results = reader.readtext(source)

    out = []
    for box, text, conf in results:
        if conf >= MIN_CONFIDENCE:
            out.append((text, float(conf), box))
    return out


def annotate(image, results):
    """Draw a box and the recognised text over each detection."""
    for text, conf, box in results:
        pts = np.array(box).astype(int)
        cv2.polylines(image, [pts], True, (0, 255, 0), 2)
        x, y = pts[0]
        cv2.putText(image, f"{text} ({conf:.0%})", (x, max(y - 8, 14)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return image


def make_test_image():
    """Build a picture with known text, so the test needs no photo."""
    img = np.full((360, 640, 3), 255, dtype=np.uint8)
    cv2.putText(img, "EXIT", (40, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 5)
    cv2.putText(img, "Room 204", (40, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 0), 3)
    cv2.putText(img, "Paracetamol 500mg", (40, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 3)
    cv2.putText(img, "Battery 12V", (40, 330),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    return img


def robot_decision(texts):
    """A robot does not want text - it wants a decision.

    This is what separates an OCR demo from an OCR application.
    """
    joined = " ".join(t.lower() for t in texts)

    if "exit" in joined:
        return "EXIT sign found -> route to the exit"
    for word in joined.split():
        if word.startswith("room"):
            return "Room number read -> navigate to that room"
    if any(k in joined for k in ("mg", "tablet", "paracetamol")):
        return "Medicine label read -> verify against the prescription"
    if "v" in joined and any(c.isdigit() for c in joined):
        return "Component label read -> log the specification"
    return "text captured -> nothing actionable"


def report(results, label=""):
    if not results:
        print(f"  {label}no text found above {MIN_CONFIDENCE:.0%} confidence")
        return []

    print(f"  {label}{len(results)} text region(s):")
    for text, conf, _ in results:
        print(f"    {conf:5.0%}  {text!r}")
    return [t for t, _, _ in results]


def self_test():
    print("=" * 58)
    print("  OCR self-test")
    print("=" * 58)

    reader = load_reader()
    image = make_test_image()
    cv2.imwrite("output_ocr_input.png", image)

    print("\n  Reading a generated sign that says:")
    print("    EXIT / Room 204 / Paracetamol 500mg / Battery 12V\n")

    start = time.time()
    results = read_text(reader, image)
    elapsed = time.time() - start

    texts = report(results)
    print(f"\n  took {elapsed:.2f}s")

    cv2.imwrite("output_ocr.png", annotate(image.copy(), results))
    print("  annotated -> output_ocr.png")

    print(f"\n  Robot decision: {robot_decision(texts)}")
    return 0


def run_image(path):
    reader = load_reader()
    image = cv2.imread(path)
    if image is None:
        print(f"Could not read '{path}'")
        return 1

    print(f"\n{path}:")
    results = read_text(reader, image)
    texts = report(results)

    cv2.imwrite("output_ocr.png", annotate(image.copy(), results))
    print("\n  annotated -> output_ocr.png")
    print(f"  Robot decision: {robot_decision(texts)}")
    return 0


def open_camera(width=1280, height=720):
    # OCR needs DETAIL, so we use a higher resolution here than the other
    # scripts. Small text simply disappears at 640x480.
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
    if "--image" in sys.argv:
        i = sys.argv.index("--image")
        if i + 1 >= len(sys.argv):
            print("Usage: python ocr_reader.py --image photo.jpg")
            sys.exit(1)
        sys.exit(run_image(sys.argv[i + 1]))

    reader = load_reader()
    cam = open_camera()
    if cam is None:
        sys.exit(1)

    # OCR is far too slow to run on every frame, so it runs on demand.
    # Real robots do the same: detect a text REGION cheaply, then read it.
    print("\n  Hold text up to the camera.")
    print("  R = read the current frame    Q = quit\n")

    results, misses = [], 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        display = annotate(frame.copy(), results) if results else frame.copy()
        cv2.rectangle(display, (0, 0), (display.shape[1], 40), (0, 0, 0), -1)
        cv2.putText(display, "R = read    Q = quit", (12, 27),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("OCR Reader", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            print("  reading ...")
            results = read_text(reader, frame)
            texts = report(results)
            print(f"  Robot decision: {robot_decision(texts)}\n")
        elif key == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
