"""
AI Robotics Bootcamp - Lesson 31
Image processing: every core operation, plus a real experiment.

Part 1 runs the standard operations and saves each result so you can open
and compare them.

Part 2 answers the lesson's mini challenge with evidence: for detecting a
coloured object under changing light, is BGR or HSV better? We test both
across five brightness levels and count what each one finds.

Needs OpenCV:
    source .venv/bin/activate
    python image_processing_demo.py
"""

import os
import sys

try:
    import cv2
    import numpy as np
except ImportError:
    print("OpenCV is not installed. Run:")
    print("    source .venv/bin/activate")
    print("    pip install opencv-python")
    sys.exit(1)

OUT = "output_processing"


# ---------------------------------------------------------------------------
# Part 1 - the operations
# ---------------------------------------------------------------------------

def make_scene(width=480, height=360, brightness=1.0):
    """A small scene: a red ball, a blue box, and some text."""
    img = np.full((height, width, 3), 235, dtype=np.uint8)

    # Remember: OpenCV uses BGR, so (blue, green, red).
    cv2.circle(img, (150, 150), 60, (40, 40, 220), -1)        # red ball
    cv2.rectangle(img, (280, 90), (420, 230), (200, 120, 40), -1)  # blue box
    cv2.putText(img, "ROBOT", (150, 320),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (30, 30, 30), 3)

    if brightness != 1.0:
        img = np.clip(img.astype(np.float32) * brightness, 0, 255).astype(np.uint8)
    return img


def part_one():
    print("=" * 62)
    print("  Part 1 - the core operations")
    print("=" * 62)

    os.makedirs(OUT, exist_ok=True)
    image = make_scene()
    steps = []

    def save(name, img, note):
        path = f"{OUT}/{name}.png"
        cv2.imwrite(path, img)
        shape = img.shape
        size = f"{shape[1]}x{shape[0]}"
        channels = shape[2] if len(shape) == 3 else 1
        steps.append((name, size, channels, note))

    save("01_original", image, "the starting image")

    # Resize - a camera gives 4032x3024, YOLO wants 640x640.
    save("02_resized", cv2.resize(image, (240, 180)), "half size, quarter the pixels")

    # Crop is just array slicing: image[y1:y2, x1:x2] - rows first!
    save("03_cropped", image[90:230, 90:230], "just the ball")

    save("04_rotated", cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),
         "for an upside-down camera mount")

    save("05_flipped", cv2.flip(image, 1), "mirror image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    save("06_gray", gray, "3 channels -> 1, three times less data")

    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    save("07_blurred", blurred, "smooths noise before edge detection")

    save("08_edges", cv2.Canny(blurred, 100, 200), "only the outlines remain")

    # Drawing - exactly how YOLO renders its detections.
    annotated = image.copy()
    cv2.rectangle(annotated, (90, 90), (210, 210), (0, 255, 0), 2)
    cv2.putText(annotated, "ball 0.96", (90, 82),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    save("09_annotated", annotated, "a bounding box, drawn the YOLO way")

    print(f"\n  {'file':<16}{'size':>10}{'ch':>4}   note")
    for name, size, channels, note in steps:
        print(f"  {name:<16}{size:>10}{channels:>4}   {note}")
    print(f"\n  Saved in {OUT}/ - open them and compare.\n")


# ---------------------------------------------------------------------------
# Part 2 - the experiment: BGR vs HSV under changing light
# ---------------------------------------------------------------------------

def count_bgr(image):
    """Find red pixels with a BGR threshold - the obvious approach."""
    lower = np.array([0, 0, 150])       # B, G, R
    upper = np.array([90, 90, 255])
    mask = cv2.inRange(image, lower, upper)
    return int(cv2.countNonZero(mask))


def count_hsv(image):
    """Find red pixels in HSV.

    HSV separates WHAT the colour is (hue) from HOW BRIGHT it is (value).
    So we can accept a wide range of brightness while still demanding the
    hue be red - which is exactly what changing light breaks in BGR.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Red sits at both ends of the hue circle, so two ranges are needed.
    lower1 = np.array([0, 100, 40])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 100, 40])
    upper2 = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)
    return int(cv2.countNonZero(mask))


def part_two():
    print("=" * 62)
    print("  Part 2 - the mini challenge, tested")
    print("=" * 62)
    print()
    print("  The same red ball, photographed at five brightness levels.")
    print("  Which colour space still finds it?\n")

    reference = None
    print(f"  {'lighting':<14}{'BGR finds':>12}{'HSV finds':>12}")
    print("  " + "-" * 38)

    bgr_ok = hsv_ok = 0

    for label, brightness in [("very bright", 1.25), ("normal", 1.0),
                              ("dim", 0.65), ("dark", 0.45),
                              ("very dark", 0.30)]:
        scene = make_scene(brightness=brightness)
        bgr = count_bgr(scene)
        hsv = count_hsv(scene)

        if reference is None:
            reference = max(hsv, 1)

        # "Found it" = at least half the expected pixels.
        bgr_found = bgr > reference * 0.5
        hsv_found = hsv > reference * 0.5
        bgr_ok += bgr_found
        hsv_ok += hsv_found

        print(f"  {label:<14}{bgr:>9} {'ok' if bgr_found else 'XX'}"
              f"{hsv:>9} {'ok' if hsv_found else 'XX'}")

        cv2.imwrite(f"{OUT}/light_{label.replace(' ', '_')}.png", scene)

    print("  " + "-" * 38)
    print(f"  {'score':<14}{bgr_ok:>9}/5{hsv_ok:>9}/5\n")

    print("  Why HSV wins:")
    print()
    print("    BGR mixes colour and brightness together. Dim the light and")
    print("    the R value falls, so a 'red' threshold stops matching - even")
    print("    though the object is obviously still red.")
    print()
    print("    HSV separates them. HUE says what the colour is, VALUE says")
    print("    how bright it is. Ask for 'red hue, any reasonable brightness'")
    print("    and the detection survives the lighting change.")
    print()
    print("  This is why robots doing colour detection convert to HSV first.")
    print("  It is also a partial answer to Lesson 29: a better colour space")
    print("  fixes the LIGHTING problem, but still cannot tell a red apple")
    print("  from a red ball. For that you need a trained model.")


if __name__ == "__main__":
    part_one()
    part_two()
