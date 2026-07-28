"""
AI Robotics Bootcamp - Lesson 42
Multi-Object Tracking (MOT): give every object a persistent ID.

Detection alone cannot tell whether the person in this frame is the same one
from the last frame. Tracking assigns each object a unique ID and keeps it
across frames - so a robot can follow "person #1" and ignore everyone else.

This uses YOLO's built-in ByteTrack (production-grade). For a transparent,
from-scratch version of the ID/lifecycle logic, see simple_tracker.py.

Usage:
    python multi_object_tracking.py --test                verify IDs persist
    python multi_object_tracking.py                       live (built-in cam)
    python multi_object_tracking.py --url http://IP:8080/video   phone camera
    python multi_object_tracking.py --follow 1            highlight only ID 1
"""

import sys
import time

try:
    import cv2
    from ultralytics import YOLO
except ImportError as e:
    print(f"Missing dependency: {e.name}")
    print("  pip install 'opencv-python<5' ultralytics")
    sys.exit(1)

MODEL_NAME = "yolo11n.pt"
CONFIDENCE = 0.5

# A distinct colour per ID, so tracks are easy to follow by eye.
PALETTE = [
    (0, 255, 0), (255, 128, 0), (0, 128, 255), (255, 0, 255),
    (0, 255, 255), (255, 255, 0), (128, 0, 255), (0, 200, 128),
]


def colour_for(track_id):
    return PALETTE[track_id % len(PALETTE)]


def draw_tracks(frame, result, follow=None, trails=None):
    """Draw each tracked box with its ID, and a short motion trail."""
    boxes = result.boxes
    if boxes is None or boxes.id is None:
        return frame, 0

    count = 0
    for box in boxes:
        tid = int(box.id[0])
        x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # When following one ID, dim everyone else.
        if follow is not None and tid != follow:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (90, 90, 90), 1)
            continue

        colour = colour_for(tid)
        cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
        cv2.putText(frame, f"ID {tid}", (x1, max(y1 - 8, 14)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2)
        count += 1

        if trails is not None:
            trails.setdefault(tid, []).append((cx, cy))
            trails[tid] = trails[tid][-30:]        # keep the last 30 points
            for p in trails[tid]:
                cv2.circle(frame, p, 2, colour, -1)

    return frame, count


def self_test():
    """Prove IDs persist across frames, without a camera.

    We shift the standard test image a little each frame to simulate motion,
    track the people in it, and check the IDs stay the same.
    """
    import urllib.request
    import numpy as np

    print("=" * 60)
    print("  Multi-object tracking self-test")
    print("=" * 60)

    model = YOLO(MODEL_NAME)
    urllib.request.urlretrieve("https://ultralytics.com/images/bus.jpg",
                               "/tmp/mot.jpg")
    base = cv2.resize(cv2.imread("/tmp/mot.jpg"), (640, 480))

    person = [i for i, n in model.names.items() if n == "person"]
    print("\n  Tracking people as the scene drifts:\n")

    id_sets = []
    for f in range(6):
        M = np.float32([[1, 0, f * 5], [0, 1, 0]])
        frame = cv2.warpAffine(base, M, (640, 480))
        r = model.track(frame, conf=CONFIDENCE, classes=person,
                        persist=True, tracker="bytetrack.yaml", verbose=False)
        b = r[0].boxes
        ids = sorted(int(x) for x in b.id.tolist()) if (b is not None and b.id is not None) else []
        id_sets.append(set(ids))
        print(f"    frame {f}: track IDs = {ids}")

    # The IDs assigned in frame 1 should still be present in the last frame.
    stable = id_sets[1] & id_sets[-1]
    print(f"\n  IDs present in both frame 1 and the last frame: {sorted(stable)}")
    print("  Persistent IDs = tracking works (vs re-detecting from scratch).")
    return 0 if stable else 1


def open_camera(source=None, width=640, height=480):
    if source is not None:
        cam = cv2.VideoCapture(source)
        if cam.isOpened():
            ok, frame = cam.read()
            if ok and frame is not None:
                where = source if isinstance(source, str) else f"index {source}"
                print(f"Camera ({where}): {frame.shape[1]}x{frame.shape[0]}")
                return cam
            cam.release()
        print(f"Could not open camera source: {source}")
        return None

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
    print("\nNo camera frames. macOS grants camera permission PER APP - run this")
    print("from the terminal inside VS Code, or enable your terminal in System")
    print("Settings > Privacy & Security > Camera, then quit (Cmd+Q) and reopen.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())

    source = None
    if "--cam" in sys.argv:
        source = int(sys.argv[sys.argv.index("--cam") + 1])
    elif "--url" in sys.argv:
        source = sys.argv[sys.argv.index("--url") + 1]

    follow = None
    if "--follow" in sys.argv:
        follow = int(sys.argv[sys.argv.index("--follow") + 1])
        print(f"Following ID {follow}; everyone else is dimmed.")

    model = YOLO(MODEL_NAME)
    cam = open_camera(source)
    if cam is None:
        sys.exit(1)

    print("  Press Q to quit.\n")
    trails, frames, started, misses = {}, 0, time.time(), 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        result = model.track(frame, conf=CONFIDENCE, persist=True,
                             tracker="bytetrack.yaml", verbose=False)[0]
        frame, shown = draw_tracks(frame, result, follow=follow, trails=trails)

        frames += 1
        fps = frames / max(time.time() - started, 1e-6)
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 34), (0, 0, 0), -1)
        cv2.putText(frame, f"{fps:.1f} fps   tracking: {shown}", (12, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Multi-Object Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
