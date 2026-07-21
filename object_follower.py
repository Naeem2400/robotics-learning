"""
AI Robotics Bootcamp - Lesson 36
Object tracking and following.

Detection alone is not enough. If the bottle moves, the robot must move
with it. This script closes that loop:

    YOLO tracking  ->  object centre  ->  compare to camera centre
                   ->  LEFT / RIGHT / FORWARD / BACK / SEARCHING

It draws the camera centre, the dead zone, and the decision on screen, so
you can watch the robot "think" as you move the object around.

No motors are attached - the decision is printed and drawn. Swapping the
print for a motor command is all that separates this from a real robot.

Usage:
    python object_follower.py                    follow a bottle (default)
    python object_follower.py --target person    follow a person
    python object_follower.py --test             no camera, checks tracking
"""

import sys

try:
    import cv2
except ImportError:
    print("OpenCV missing.  pip install 'opencv-python<5'")
    sys.exit(1)

try:
    from ultralytics import YOLO
except ImportError:
    print("Ultralytics missing.  pip install ultralytics")
    sys.exit(1)

MODEL_NAME = "yolo11n.pt"
CONFIDENCE = 0.45

# How far off-centre the object may drift before the robot turns.
# Too small and the robot twitches constantly; too large and it drifts.
# This is the same hysteresis idea as the obstacle avoider in Lesson 26.
DEAD_ZONE = 60          # pixels either side of centre

# The box area is a rough stand-in for distance: a bigger box means closer.
TOO_CLOSE = 0.25        # box covers more than 25% of the frame -> back off
TOO_FAR = 0.04          # less than 4% -> approach


def decide(object_x, object_area_ratio, frame_width):
    """Turn a detection into one robot command.

    This is the whole lesson in one function.
    """
    centre = frame_width / 2
    error = object_x - centre          # negative = object is left of centre

    if abs(error) > DEAD_ZONE:
        return ("TURN LEFT", error) if error < 0 else ("TURN RIGHT", error)

    # Lined up. Now worry about distance.
    if object_area_ratio > TOO_CLOSE:
        return "BACK UP", error
    if object_area_ratio < TOO_FAR:
        return "FORWARD", error
    return "HOLD", error


def draw_hud(frame, target, decision, error, track_id, area_ratio):
    """Draw the centre line, dead zone and decision."""
    h, w = frame.shape[:2]
    centre = w // 2

    # Dead zone band
    cv2.rectangle(frame, (centre - DEAD_ZONE, 0), (centre + DEAD_ZONE, h),
                  (60, 60, 60), 1)
    cv2.line(frame, (centre, 0), (centre, h), (200, 200, 200), 1)

    colour = {
        "TURN LEFT": (0, 200, 255),
        "TURN RIGHT": (0, 200, 255),
        "FORWARD": (0, 255, 0),
        "BACK UP": (0, 120, 255),
        "HOLD": (0, 255, 0),
        "SEARCHING": (0, 0, 255),
    }.get(decision, (255, 255, 255))

    cv2.rectangle(frame, (0, 0), (w, 46), (0, 0, 0), -1)
    label = f"{decision}"
    if track_id is not None:
        label += f"   {target} id:{track_id}   offset:{error:+.0f}px" \
                 f"   size:{area_ratio:.0%}"
    cv2.putText(frame, label, (12, 32), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, colour, 2)
    return frame


def self_test():
    print("=" * 58)
    print("  Object follower self-test")
    print("=" * 58)

    model = YOLO(MODEL_NAME)
    names = {n.lower() for n in model.names.values()}
    print(f"  Model loaded, {len(model.names)} classes")
    print(f"  'bottle' available: {'bottle' in names}")
    print(f"  'person' available: {'person' in names}")

    print("\n  Decision logic (frame width 640, centre 320):")
    for x, area in [(90, 0.10), (320, 0.10), (540, 0.10),
                    (320, 0.35), (320, 0.02)]:
        d, err = decide(x, area, 640)
        print(f"    object at x={x:>3}, size {area:>4.0%} -> {d:<10} "
              f"(offset {err:+.0f})")

    print("\n  Matches the lesson: object at 90 -> LEFT, 540 -> RIGHT.")
    return 0


def open_camera(width=640, height=480):
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
    print("\nNo camera frames. macOS grants camera permission PER APP -")
    print("run this from the terminal inside VS Code, or enable your terminal")
    print("in System Settings > Privacy & Security > Camera, then fully quit")
    print("it (Cmd+Q) and reopen.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())

    target = "bottle"
    if "--target" in sys.argv:
        i = sys.argv.index("--target")
        if i + 1 < len(sys.argv):
            target = sys.argv[i + 1].lower()

    model = YOLO(MODEL_NAME)
    wanted = [i for i, n in model.names.items() if n.lower() == target]
    if not wanted:
        print(f"'{target}' is not a class this model knows.")
        sys.exit(1)
    print(f"Following: {target}")

    cam = open_camera()
    if cam is None:
        sys.exit(1)

    print("  Press Q to quit.\n")
    last_decision = None
    misses = 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        h, w = frame.shape[:2]

        # persist=True keeps track IDs stable between frames - that is the
        # difference between tracking and just detecting again each frame.
        results = model.track(frame, conf=CONFIDENCE, classes=wanted,
                              persist=True, tracker="bytetrack.yaml",
                              verbose=False)

        boxes = results[0].boxes
        decision, error, track_id, area_ratio = "SEARCHING", 0.0, None, 0.0

        if boxes is not None and len(boxes) > 0:
            # If several are visible, follow the biggest (nearest) one.
            areas = [(float(b.xywh[0][2] * b.xywh[0][3]), i)
                     for i, b in enumerate(boxes)]
            _, best = max(areas)
            box = boxes[best]

            x_centre = float(box.xywh[0][0])
            area_ratio = float(box.xywh[0][2] * box.xywh[0][3]) / (w * h)
            track_id = int(box.id[0]) if box.id is not None else None
            decision, error = decide(x_centre, area_ratio, w)

        annotated = results[0].plot()
        annotated = draw_hud(annotated, target, decision, error,
                             track_id, area_ratio)

        if decision != last_decision:
            print(f"  {decision:<10} offset {error:+6.0f}px  size {area_ratio:.0%}")
            last_decision = decision

        cv2.imshow("Object Following", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
