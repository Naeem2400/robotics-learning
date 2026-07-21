"""
AI Robotics Bootcamp - Lesson 37
Human pose estimation: the robot builds a digital skeleton of a person.

Object detection tells the robot "a person is there". Pose estimation tells
it what that person is DOING - which is what you need before a robot can
react to a raised hand, spot someone who has fallen, or count squats.

This uses YOLO pose, which needs no extra installation because ultralytics
is already set up. MediaPipe is a good alternative - see the lesson notes.

Usage:
    python pose_estimation.py --test        check the model, no camera
    python pose_estimation.py --image f.jpg run on one image
    python pose_estimation.py               live camera
"""

import sys

try:
    import cv2
    from ultralytics import YOLO
except ImportError as e:
    print(f"Missing dependency: {e.name}")
    print("  source .venv/bin/activate")
    print("  pip install 'opencv-python<5' ultralytics")
    sys.exit(1)

MODEL_NAME = "yolo11n-pose.pt"
CONFIDENCE = 0.5

# The 17 COCO keypoints, in the order the model returns them.
KEYPOINTS = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]
IDX = {name: i for i, name in enumerate(KEYPOINTS)}


def read_pose(keypoints_xy, confidences, threshold=0.5):
    """Turn raw keypoint arrays into a {name: (x, y)} dict.

    Low-confidence points are dropped - a hidden wrist gives nonsense
    coordinates, and acting on those is a classic beginner bug.
    """
    points = {}
    for i, name in enumerate(KEYPOINTS):
        if confidences is None or float(confidences[i]) >= threshold:
            x, y = float(keypoints_xy[i][0]), float(keypoints_xy[i][1])
            if x > 0 or y > 0:
                points[name] = (x, y)
    return points


def describe_pose(points):
    """Read a simple gesture out of the skeleton.

    Image coordinates run DOWNWARD, so a raised hand means the wrist has a
    SMALLER y than the shoulder. Getting that backwards is the usual error.
    """
    gestures = []

    for side in ("left", "right"):
        wrist = points.get(f"{side}_wrist")
        shoulder = points.get(f"{side}_shoulder")
        if wrist and shoulder and wrist[1] < shoulder[1]:
            gestures.append(f"{side} hand raised")

    if len(gestures) == 2:
        return "BOTH HANDS UP"
    if gestures:
        return gestures[0].upper()

    # Rough fall check: shoulders and hips at nearly the same height means
    # the person is horizontal rather than upright.
    ls, rs = points.get("left_shoulder"), points.get("right_shoulder")
    lh, rh = points.get("left_hip"), points.get("right_hip")
    if ls and rs and lh and rh:
        shoulder_y = (ls[1] + rs[1]) / 2
        hip_y = (lh[1] + rh[1]) / 2
        shoulder_width = abs(ls[0] - rs[0]) or 1
        if abs(hip_y - shoulder_y) < shoulder_width * 0.4:
            return "PERSON MAY HAVE FALLEN"

    return "standing"


def annotate(frame, result):
    """Draw the skeleton plus a readable gesture label per person."""
    out = result.plot()          # ultralytics draws the skeleton for us
    kps = result.keypoints

    if kps is not None and kps.xy is not None:
        for i in range(len(kps.xy)):
            conf = kps.conf[i] if kps.conf is not None else None
            points = read_pose(kps.xy[i], conf)
            gesture = describe_pose(points)

            head = points.get("nose")
            x, y = (int(head[0]) - 40, int(head[1]) - 30) if head else (12, 30 + i * 30)
            colour = (0, 255, 0) if gesture == "standing" else (0, 200, 255)
            cv2.putText(out, gesture, (max(x, 5), max(y, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2)
    return out


def self_test():
    print("=" * 58)
    print("  Pose estimation self-test")
    print("=" * 58)

    model = YOLO(MODEL_NAME)
    print(f"  Model      : {MODEL_NAME}")
    print(f"  Keypoints  : {len(KEYPOINTS)} per person")
    print(f"  Names      : {', '.join(KEYPOINTS[:6])} ...")

    print("\n  Gesture logic (y increases DOWNWARD in an image):")
    cases = [
        ("hand raised", {"left_wrist": (100, 50), "left_shoulder": (100, 200)}),
        ("hand down",   {"left_wrist": (100, 300), "left_shoulder": (100, 200)}),
        ("both up",     {"left_wrist": (80, 40), "left_shoulder": (80, 200),
                         "right_wrist": (160, 40), "right_shoulder": (160, 200)}),
    ]
    for label, pts in cases:
        print(f"    {label:<12} -> {describe_pose(pts)}")
    return 0


def run_image(path):
    model = YOLO(MODEL_NAME)
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read '{path}'")
        return 1

    result = model(img, conf=CONFIDENCE, verbose=False)[0]
    people = len(result.boxes) if result.boxes is not None else 0
    print(f"\n{path}: {people} person(s)")

    kps = result.keypoints
    if kps is not None:
        for i in range(len(kps.xy)):
            conf = kps.conf[i] if kps.conf is not None else None
            points = read_pose(kps.xy[i], conf)
            print(f"  person {i + 1}: {len(points)}/17 keypoints visible "
                  f"-> {describe_pose(points)}")

    cv2.imwrite("output_pose.jpg", annotate(img, result))
    print("\n  Saved output_pose.jpg")
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
    print("\nNo camera frames. macOS grants camera permission PER APP - run")
    print("this from the terminal inside VS Code, or enable your terminal in")
    print("System Settings > Privacy & Security > Camera, then fully quit")
    print("it (Cmd+Q) and reopen.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())
    if "--image" in sys.argv:
        i = sys.argv.index("--image")
        if i + 1 >= len(sys.argv):
            print("Usage: python pose_estimation.py --image photo.jpg")
            sys.exit(1)
        sys.exit(run_image(sys.argv[i + 1]))

    model = YOLO(MODEL_NAME)
    cam = open_camera()
    if cam is None:
        sys.exit(1)

    print("  Raise a hand and watch the label change. Press Q to quit.\n")
    last = None
    misses = 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        result = model(frame, conf=CONFIDENCE, verbose=False)[0]
        out = annotate(frame, result)

        kps = result.keypoints
        gesture = "no person"
        if kps is not None and kps.xy is not None and len(kps.xy) > 0:
            conf = kps.conf[0] if kps.conf is not None else None
            gesture = describe_pose(read_pose(kps.xy[0], conf))
        if gesture != last:
            print(f"  {gesture}")
            last = gesture

        cv2.imshow("Pose Estimation", out)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
