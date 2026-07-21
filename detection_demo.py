"""
AI Robotics Bootcamp - Lesson 16
Bounding boxes and confidence scores - without needing YOLO installed.

YOLO's output is just a list of detections. Each one is:

    label, confidence, and a box (x1, y1, x2, y2)

This script takes detections in exactly that format, applies the confidence
threshold a real robot would use, draws the bounding boxes, and prints the
robot's decision. Once ultralytics is installed, the ONLY thing that changes
is where the detections come from - the logic below stays identical.

Uses no libraries, so it runs today.

Run with:
    python3 detection_demo.py
"""

import struct
import zlib

WIDTH = 320
HEIGHT = 240
CONFIDENCE_THRESHOLD = 0.80      # the robot ignores anything less certain

# What YOLO would hand back: (label, confidence, x1, y1, x2, y2)
DETECTIONS = [
    ("person", 0.99, 30, 60, 110, 220),
    ("bottle", 0.96, 150, 120, 190, 205),
    ("chair", 0.94, 215, 90, 300, 215),
    ("cat", 0.52, 130, 20, 175, 60),      # too uncertain - will be ignored
]

COLOURS = {
    "person": (230, 70, 70),
    "bottle": (70, 190, 90),
    "chair": (80, 130, 230),
    "cat": (180, 180, 180),
}


def blank_scene():
    """A plain background to draw the boxes onto."""
    return [[(240, 240, 235) for _ in range(WIDTH)] for _ in range(HEIGHT)]


def fill_box(pixels, x1, y1, x2, y2, colour):
    """Solid rectangle - stands in for the object itself."""
    for y in range(max(0, y1), min(HEIGHT, y2)):
        for x in range(max(0, x1), min(WIDTH, x2)):
            pixels[y][x] = colour


def draw_box_outline(pixels, x1, y1, x2, y2, colour, thickness=3):
    """Draw only the outline - this is what a bounding box looks like."""
    for t in range(thickness):
        for x in range(max(0, x1), min(WIDTH, x2)):
            for y in (y1 + t, y2 - 1 - t):
                if 0 <= y < HEIGHT:
                    pixels[y][x] = colour
        for y in range(max(0, y1), min(HEIGHT, y2)):
            for x in (x1 + t, x2 - 1 - t):
                if 0 <= x < WIDTH:
                    pixels[y][x] = colour


def write_png(path, pixels):
    """Write RGB rows to a real .png file (standard library only)."""
    raw = b""
    for row in pixels:
        raw += b"\x00" + bytes(v for px in row for v in px)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def box_area(x1, y1, x2, y2):
    return (x2 - x1) * (y2 - y1)


def main():
    print("=" * 62)
    print("  Lesson 16 - Bounding boxes and confidence")
    print("=" * 62)
    print(f"\nConfidence threshold: {CONFIDENCE_THRESHOLD:.0%}\n")

    scene = blank_scene()
    kept, rejected = [], []

    for label, confidence, x1, y1, x2, y2 in DETECTIONS:
        colour = COLOURS.get(label, (120, 120, 120))
        centre_x = (x1 + x2) // 2
        centre_y = (y1 + y2) // 2

        if confidence >= CONFIDENCE_THRESHOLD:
            kept.append((label, confidence, centre_x, centre_y))
            fill_box(scene, x1, y1, x2, y2, colour)
            draw_box_outline(scene, x1, y1, x2, y2, (20, 20, 20))
            mark = "ACCEPT"
        else:
            rejected.append((label, confidence))
            mark = "REJECT"

        print(f"  {mark}  {label:<8} {confidence:5.0%}  "
              f"box=({x1:3},{y1:3})-({x2:3},{y2:3})  "
              f"centre=({centre_x:3},{centre_y:3})  "
              f"area={box_area(x1, y1, x2, y2):,}px")

    write_png("output_detections.png", scene)

    print(f"\n  Kept {len(kept)}, rejected {len(rejected)}.")
    print("  Saved output_detections.png - open it to see the boxes.\n")

    # ---- The robot's decision ------------------------------------------
    print("-" * 62)
    print("ROBOT DECISION")
    print("-" * 62)

    names = [label for label, *_ in kept]

    if "person" in names:
        # Safety first - the same priority rule as Lesson 10.
        print("  A person was detected -> stop and keep a safe distance.")
    elif "bottle" in names:
        label, confidence, cx, cy = next(k for k in kept if k[0] == "bottle")
        side = "left" if cx < WIDTH // 2 else "right"
        print(f"  Bottle found at ({cx}, {cy}), {side} of centre -> "
              f"turn {side} and approach.")
    else:
        print("  Nothing to act on -> keep searching.")

    if rejected:
        ignored = ", ".join(f"{n} ({c:.0%})" for n, c in rejected)
        print(f"\n  Ignored as too uncertain: {ignored}")
        print("  A low threshold makes the robot jumpy; a high one makes it")
        print("  miss things. Choosing it is a real engineering decision.")


if __name__ == "__main__":
    main()
