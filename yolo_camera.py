"""
AI Robotics Bootcamp - Lesson 34/35
Live object detection with YOLO.

The robot stops seeing "pixels" and starts seeing "a person, a laptop,
a bottle" - each with a box and a confidence score.

Usage:
    python yolo_camera.py --test        check the model loads (no camera)
    python yolo_camera.py --image f.jpg detect on one image file
    python yolo_camera.py               live camera, press Q to quit

The first run downloads the model weights (~6 MB) once, then works offline.
"""

import sys
import time

try:
    import cv2
except ImportError:
    print("OpenCV missing.  source .venv/bin/activate && pip install 'opencv-python<5'")
    sys.exit(1)

try:
    from ultralytics import YOLO
except ImportError:
    print("Ultralytics (YOLO) is not installed.\n")
    print("    source .venv/bin/activate")
    print("    pip install ultralytics\n")
    print("Note: this pulls in PyTorch and is a large download.")
    print("Meanwhile, detection_demo.py teaches boxes and confidence")
    print("with no installation at all.")
    sys.exit(1)

MODEL_NAME = "yolo11n.pt"       # 'n' = nano: smallest and fastest, good on an M1
CONFIDENCE = 0.5                # ignore anything the model is unsure about


def load_model():
    print(f"Loading {MODEL_NAME} ...")
    model = YOLO(MODEL_NAME)
    print(f"Model loaded. It knows {len(model.names)} object classes.")
    return model


def describe(result, model, label=""):
    """Print what was detected, in plain language."""
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        print(f"  {label}nothing detected above {CONFIDENCE:.0%} confidence")
        return 0

    print(f"  {label}{len(boxes)} object(s):")
    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
        print(f"    {model.names[cls]:<12} {conf:5.0%}  "
              f"box ({x1:4},{y1:4}) - ({x2:4},{y2:4})")
    return len(boxes)


def self_test():
    """Verify the model loads and runs. Uses a generated image, not the camera."""
    import numpy as np

    print("=" * 58)
    print("  YOLO self-test")
    print("=" * 58)

    model = load_model()

    # A few of the classes YOLO knows, for context.
    sample = [model.names[i] for i in sorted(model.names)[:12]]
    print(f"  Some classes: {', '.join(sample)} ...")

    # Run on a blank image just to prove the pipeline executes.
    blank = np.full((480, 640, 3), 200, dtype=np.uint8)
    start = time.time()
    results = model(blank, conf=CONFIDENCE, verbose=False)
    elapsed = time.time() - start

    print(f"\n  Inference on a 640x480 frame took {elapsed * 1000:.0f} ms "
          f"({1 / max(elapsed, 1e-6):.1f} fps)")
    describe(results[0], model, label="Blank image: ")
    print("\n  Pipeline works. Run with --image or no arguments.")
    return 0


def detect_image(path):
    model = load_model()
    image = cv2.imread(path)
    if image is None:
        print(f"Could not read '{path}'")
        return 1

    results = model(image, conf=CONFIDENCE, verbose=False)
    print(f"\n{path}:")
    describe(results[0], model)

    annotated = results[0].plot()          # draws boxes and labels for you
    out = "output_yolo.jpg"
    cv2.imwrite(out, annotated)
    print(f"\n  Annotated image saved to {out}")
    return 0


def open_camera(width=640, height=480):
    for index in (0, 1, 2):
        camera = cv2.VideoCapture(index)
        if camera.isOpened():
            # Set the size BEFORE the first read. Changing it afterwards can
            # make the next few frames come back empty on macOS.
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            ok, frame = camera.read()
            if ok and frame is not None:
                print(f"Camera {index}: {frame.shape[1]}x{frame.shape[0]}")
                return camera
            camera.release()
        # Index 0 not opening usually means permission, not a missing camera.
        if index == 0:
            break

    print("\nCould not get frames from the camera.")
    print("\nOn macOS, camera permission is granted PER APPLICATION.")
    print("Whichever app launched this script needs its own permission -")
    print("granting it to VS Code does NOT cover Terminal, and vice versa.")
    print("\nEasiest fix: run this from the terminal INSIDE VS Code,")
    print("which usually already has camera access.")
    print("\nOtherwise: System Settings > Privacy & Security > Camera,")
    print("enable your terminal app, then FULLY QUIT it (Cmd+Q) and reopen -")
    print("macOS only applies the change when the app next launches.")
    print("\nAlso check no other app (Zoom, Teams, FaceTime) holds the camera.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())

    if "--image" in sys.argv:
        i = sys.argv.index("--image")
        if i + 1 >= len(sys.argv):
            print("Usage: python yolo_camera.py --image photo.jpg")
            sys.exit(1)
        sys.exit(detect_image(sys.argv[i + 1]))

    # Homework: --only person,bottle  shows just those classes.
    keep = None
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        if i + 1 < len(sys.argv):
            keep = {n.strip().lower() for n in sys.argv[i + 1].split(",")}

    model = load_model()

    if keep:
        # YOLO wants class NUMBERS, not names, so translate.
        wanted = [i for i, name in model.names.items() if name.lower() in keep]
        if not wanted:
            print(f"None of {sorted(keep)} are classes this model knows.")
            sys.exit(1)
        print(f"Showing only: {', '.join(model.names[i] for i in wanted)}")
    else:
        wanted = None

    # 640x480 keeps an 8 GB M1 comfortable.
    camera = open_camera(640, 480)
    if camera is None:
        sys.exit(1)

    print("  Press Q to quit.\n")
    frames = 0
    fps = 0.0                 # defined up front, so the summary always works
    started = time.time()
    misses = 0

    while True:
        ok, frame = camera.read()
        if not ok or frame is None:
            # A dropped frame now and then is normal; only give up if the
            # camera goes away for good.
            misses += 1
            if misses > 30:
                print("  Lost the camera feed.")
                break
            time.sleep(0.05)
            continue
        misses = 0

        results = model(frame, conf=CONFIDENCE, classes=wanted, verbose=False)
        annotated = results[0].plot()

        frames += 1
        fps = frames / max(time.time() - started, 1e-6)
        count = 0 if results[0].boxes is None else len(results[0].boxes)

        cv2.putText(annotated, f"{fps:.1f} fps   objects: {count}",
                    (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("YOLO Object Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    if frames:
        print(f"\n  Processed {frames} frames at about {fps:.1f} fps.")
    else:
        print("\n  No frames were processed.")


if __name__ == "__main__":
    main()
