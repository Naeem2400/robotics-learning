"""
AI Robotics Bootcamp - Lesson 38
Hand tracking and gesture recognition.

MediaPipe gives 21 landmarks per hand. This script turns those landmarks
into finger states (up/down), the finger states into a gesture, and the
gesture into a robot command.

    camera -> 21 landmarks -> fingers up -> gesture -> robot command

Usage:
    python hand_gestures.py --test    gesture logic only, no camera
    python hand_gestures.py           live camera, press Q to quit
"""

import sys

try:
    import cv2
except ImportError:
    print("OpenCV missing.  pip install 'opencv-python<5'")
    sys.exit(1)

MODEL_PATH = "models/hand_landmarker.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
             "hand_landmarker/float16/1/hand_landmarker.task")


def build_detector():
    """Create a MediaPipe HandLandmarker.

    NOTE: MediaPipe 0.10.35 REMOVED the old `mp.solutions.hands` API that
    almost every tutorial still uses. The current interface is the Tasks
    API below, which needs a downloaded .task model file.
    """
    import os
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
    except ImportError:
        print("MediaPipe is not installed. Install it WITH the version pin:\n")
        print('    pip install mediapipe "opencv-contrib-python<5"\n')
        print("The pin matters: without it pip installs OpenCV 5, which removes")
        print("CascadeClassifier and breaks the face detection from Lesson 32.")
        sys.exit(1)

    if not os.path.exists(MODEL_PATH):
        print(f"Model missing. Download it once with:\n")
        print(f"  mkdir -p models && curl -L -o {MODEL_PATH} \\")
        print(f"    {MODEL_URL}\n")
        sys.exit(1)

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
        num_hands=1)
    return mp, vision.HandLandmarker.create_from_options(options)

# MediaPipe's 21 hand landmarks. We only need the tips and the joint below
# each tip (the "pip" joint) to decide whether a finger is extended.
TIPS = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "little": 20}
PIPS = {"thumb": 3, "index": 6, "middle": 10, "ring": 14, "little": 18}
FINGER_ORDER = ["thumb", "index", "middle", "ring", "little"]

# What each gesture tells the robot to do. Change these freely.
COMMANDS = {
    "FIST": "STOP",
    "ONE": "FORWARD",
    "PEACE": "TAKE PHOTO",
    "THREE": "TURN LEFT",
    "FOUR": "TURN RIGHT",
    "OPEN PALM": "START",
    "THUMBS UP": "CONFIRM",
}


def fingers_up(landmarks, handedness):
    """Return {finger: True/False} for one hand.

    For the four fingers: a finger is extended when its TIP is higher up the
    image (smaller y) than the joint below it.

    The thumb is different - it folds sideways, not down - so it needs an x
    comparison, and the direction flips depending on which hand it is. This
    is the detail most tutorials get wrong.
    """
    state = {}

    for finger in ["index", "middle", "ring", "little"]:
        tip = landmarks[TIPS[finger]]
        pip = landmarks[PIPS[finger]]
        state[finger] = tip.y < pip.y

    thumb_tip = landmarks[TIPS["thumb"]]
    thumb_pip = landmarks[PIPS["thumb"]]
    if handedness == "Right":
        state["thumb"] = thumb_tip.x < thumb_pip.x
    else:
        state["thumb"] = thumb_tip.x > thumb_pip.x

    return state


def classify(state):
    """Turn finger states into a named gesture."""
    up = [f for f in FINGER_ORDER if state.get(f)]
    count = len(up)

    if count == 0:
        return "FIST", 0
    if up == ["thumb"]:
        return "THUMBS UP", 1
    if up == ["index"]:
        return "ONE", 1
    if up == ["index", "middle"]:
        return "PEACE", 2
    if up == ["index", "middle", "ring"]:
        return "THREE", 3
    if up == ["index", "middle", "ring", "little"]:
        return "FOUR", 4
    if count == 5:
        return "OPEN PALM", 5
    return f"{count} FINGERS", count


CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),            # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),            # index
    (5, 9), (9, 10), (10, 11), (11, 12),       # middle
    (9, 13), (13, 14), (14, 15), (15, 16),     # ring
    (13, 17), (17, 18), (18, 19), (19, 20),    # little
    (0, 17),                                    # palm edge
]


def draw_hand(frame, landmarks):
    """Draw the 21 landmarks and the bones between them.

    The Tasks API returns NORMALISED coordinates (0-1), so they must be
    multiplied by the frame size before drawing.
    """
    h, w = frame.shape[:2]
    pts = [(int(p.x * w), int(p.y * h)) for p in landmarks]

    for a, b in CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 200, 0), 2)
    for i, (x, y) in enumerate(pts):
        colour = (0, 0, 255) if i in TIPS.values() else (255, 200, 0)
        cv2.circle(frame, (x, y), 5, colour, -1)


def self_test():
    """Check the gesture logic without a camera."""
    print("=" * 58)
    print("  Hand gesture self-test")
    print("=" * 58)
    print("\n  finger states -> gesture -> robot command\n")

    cases = [
        ("fist",        dict(thumb=0, index=0, middle=0, ring=0, little=0)),
        ("thumbs up",   dict(thumb=1, index=0, middle=0, ring=0, little=0)),
        ("point",       dict(thumb=0, index=1, middle=0, ring=0, little=0)),
        ("peace",       dict(thumb=0, index=1, middle=1, ring=0, little=0)),
        ("three",       dict(thumb=0, index=1, middle=1, ring=1, little=0)),
        ("four",        dict(thumb=0, index=1, middle=1, ring=1, little=1)),
        ("open palm",   dict(thumb=1, index=1, middle=1, ring=1, little=1)),
    ]

    for label, raw in cases:
        state = {k: bool(v) for k, v in raw.items()}
        gesture, count = classify(state)
        command = COMMANDS.get(gesture, "-")
        bits = "".join("1" if state[f] else "0" for f in FINGER_ORDER)
        print(f"    {label:<11} [{bits}]  {count} up  ->  "
              f"{gesture:<10} -> {command}")

    print("\n  (bit order: thumb, index, middle, ring, little)")
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
    print("System Settings > Privacy & Security > Camera, then fully quit it")
    print("(Cmd+Q) and reopen.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())

    mp, detector = build_detector()

    cam = open_camera()
    if cam is None:
        sys.exit(1)

    print("\n  Show a gesture. Press Q to quit.")
    print("  fist=STOP  1=FORWARD  peace=PHOTO  palm=START  thumb=CONFIRM\n")

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

        # Mirror so moving your hand right moves it right on screen.
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(image)

        gesture, command = "no hand", "-"

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]

            label = "Right"
            if result.handedness:
                label = result.handedness[0][0].category_name
            # The frame was mirrored, so flip the reported hand back.
            label = "Left" if label == "Right" else "Right"

            state = fingers_up(landmarks, label)
            gesture, _count = classify(state)
            command = COMMANDS.get(gesture, "-")

            draw_hand(frame, landmarks)

            bits = " ".join(f"{f[:3]}:{'^' if state[f] else 'v'}"
                            for f in FINGER_ORDER)
            cv2.putText(frame, bits, (12, frame.shape[0] - 14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.rectangle(frame, (0, 0), (frame.shape[1], 60), (0, 0, 0), -1)
        colour = (0, 255, 0) if command != "-" else (120, 120, 120)
        cv2.putText(frame, gesture, (12, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, colour, 2)
        cv2.putText(frame, f"robot: {command}", (12, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2)

        if gesture != last:
            print(f"  {gesture:<12} -> {command}")
            last = gesture

        cv2.imshow("Hand Gestures", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
