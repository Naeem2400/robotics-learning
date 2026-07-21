"""
AI Robotics Bootcamp - Lesson 32
Face detection with Haar cascades.

Detection answers "is there a face, and where?" - NOT "whose face is it?"
That second question is recognition, and it is a much harder problem.

Usage:
    python face_detection.py            live camera with green boxes
    python face_detection.py --test     check the cascade loads, no camera
    python face_detection.py --check    detect on ONE camera frame, report
                                        only the count (no image saved)

Nothing is ever written to disk by --test or --check.
"""

import sys

try:
    import cv2
except ImportError:
    print("OpenCV is not installed. Run:")
    print("    source .venv/bin/activate")
    print("    pip install 'opencv-python<5'")
    sys.exit(1)

CASCADE_FILE = "haarcascade_frontalface_default.xml"

# Tuning knobs for detectMultiScale:
#   scaleFactor  how much the image shrinks at each pass. 1.1 = 10% steps.
#                Smaller = more thorough but slower.
#   minNeighbors how many overlapping detections are needed to accept a face.
#                Higher = fewer false positives, but misses more faces.
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_SIZE = (60, 60)


def load_cascade():
    """Load the face cascade, or explain clearly why it failed."""
    if not hasattr(cv2, "CascadeClassifier"):
        print("This OpenCV build has no CascadeClassifier.")
        print("OpenCV 5.0 removed it. Install version 4:")
        print("    pip install 'opencv-python<5'")
        return None

    path = cv2.data.haarcascades + CASCADE_FILE
    cascade = cv2.CascadeClassifier(path)

    # CascadeClassifier does NOT raise on a bad path - it returns an empty
    # classifier that silently detects nothing. Always check empty().
    if cascade.empty():
        print(f"Cascade failed to load from:\n  {path}")
        return None

    return cascade


def detect(cascade, frame):
    """Return a list of face boxes as (x, y, width, height)."""
    # Haar cascades work on brightness, not colour, so convert first.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cascade.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=MIN_SIZE,
    )


def open_camera():
    for index in (0, 1, 2):
        camera = cv2.VideoCapture(index)
        if camera.isOpened():
            ok, frame = camera.read()
            if ok and frame is not None:
                return camera
            camera.release()
    print("No camera frames. macOS grants camera permission PER APP -\n"
          "  try running from the terminal inside VS Code, or enable your\n"
          "  terminal in System Settings > Privacy & Security > Camera\n"
          "  and fully quit (Cmd+Q) and reopen it.")
    return None


def self_test():
    """Verify the cascade loads. Does not touch the camera."""
    print("=" * 54)
    print("  Face detection self-test")
    print("=" * 54)
    print(f"  OpenCV version : {cv2.__version__}")

    cascade = load_cascade()
    if cascade is None:
        return 1

    print(f"  Cascade file   : {CASCADE_FILE}")
    print("  Loaded         : yes")
    print("\n  Ready. Run with --check to test one camera frame,")
    print("  or with no arguments for the live window.")
    return 0


def check_one_frame():
    """Grab ONE frame, count faces, report numbers only.

    No image is saved, displayed, or transmitted - only how many faces were
    found and how big they were.
    """
    print("=" * 54)
    print("  Single-frame check (no image is saved)")
    print("=" * 54)

    cascade = load_cascade()
    if cascade is None:
        return 1

    camera = open_camera()
    if camera is None:
        return 1

    ok, frame = camera.read()
    camera.release()
    if not ok:
        print("  Could not read a frame.")
        return 1

    faces = detect(cascade, frame)
    height, width = frame.shape[:2]

    print(f"  Frame          : {width} x {height}")
    print(f"  Faces detected : {len(faces)}")
    for i, (x, y, w, h) in enumerate(faces, 1):
        pct = 100.0 * (w * h) / (width * height)
        print(f"    face {i}: box ({x}, {y}) size {w}x{h} "
              f"- {pct:.1f}% of the frame")

    if len(faces) == 0:
        print("\n  No face found. That is not necessarily a bug - Haar")
        print("  cascades need a reasonably lit, front-facing face.")
    return 0


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())
    if "--check" in sys.argv:
        sys.exit(check_one_frame())

    cascade = load_cascade()
    if cascade is None:
        sys.exit(1)

    camera = open_camera()
    if camera is None:
        sys.exit(1)

    print("  Press Q to quit.\n")

    while True:
        ok, frame = camera.read()
        if not ok:
            break

        faces = detect(cascade, frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "face", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, f"faces: {len(faces)}", (12, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 0), 2)

        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
