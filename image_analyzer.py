"""
AI Robotics Bootcamp - Lesson 14
Image Analyzer - the OpenCV mini project.

Runs the standard robot-vision pipeline on an image:

    load -> resize -> grayscale -> blur -> edge detection

Every step is saved to the output/ folder so you can open the files and
compare them. Nothing is displayed in a window, because cv2.imshow() is
unreliable on macOS - saving files works everywhere.

Usage:
    python3 image_analyzer.py                 # uses a generated sample image
    python3 image_analyzer.py photo.jpg       # uses your own image
"""

import os
import sys

import cv2
import numpy as np

OUTPUT_DIR = "output"
RESIZE_TO = (640, 480)


def make_sample_image(width=800, height=600):
    """Draw a simple scene so the script works without any photo.

    An image in OpenCV is just a NumPy array of numbers - exactly what
    Lesson 13 showed. Here we start from a blank array and draw on it.
    """
    image = np.full((height, width, 3), 235, dtype=np.uint8)   # light background

    # OpenCV uses BGR order, not RGB. This is the classic beginner trap.
    cv2.rectangle(image, (80, 120), (330, 380), (60, 60, 200), -1)     # red box
    cv2.circle(image, (560, 220), 110, (200, 140, 40), -1)             # blue circle
    cv2.line(image, (60, 500), (740, 470), (40, 160, 40), 12)          # green line
    cv2.putText(image, "ROBOT VISION", (200, 560),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (30, 30, 30), 3)

    return image


def describe(image, label):
    """Print what an image actually is: numbers in an array."""
    if image.ndim == 3:
        height, width, channels = image.shape
    else:
        height, width = image.shape
        channels = 1

    total = height * width
    print(f"  {label:<12} {width} x {height}, {channels} channel(s), "
          f"{total * channels:,} numbers")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ---- 1. Load ---------------------------------------------------------
    if len(sys.argv) > 1:
        path = sys.argv[1]
        image = cv2.imread(path)
        if image is None:
            # imread returns None instead of raising - a very common trap.
            print(f"Could not read '{path}'. Check the file path.")
            return
        print(f"Loaded {path}")
    else:
        image = make_sample_image()
        cv2.imwrite(f"{OUTPUT_DIR}/1_original.png", image)
        print("No image given, so a sample image was generated.")

    print("\nThe pipeline:")
    describe(image, "original")

    # ---- 2. Resize -------------------------------------------------------
    # Smaller image = fewer numbers = faster robot. This is a real tradeoff.
    resized = cv2.resize(image, RESIZE_TO)
    describe(resized, "resized")
    cv2.imwrite(f"{OUTPUT_DIR}/2_resized.png", resized)

    # ---- 3. Grayscale ----------------------------------------------------
    # Three numbers per pixel become one: 3x less data to process.
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    describe(gray, "grayscale")
    cv2.imwrite(f"{OUTPUT_DIR}/3_gray.png", gray)

    # ---- 4. Blur ---------------------------------------------------------
    # Removes noise. Without this, edge detection finds fake edges in specks.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    describe(blurred, "blurred")
    cv2.imwrite(f"{OUTPUT_DIR}/4_blurred.png", blurred)

    # ---- 5. Edge detection -----------------------------------------------
    # The robot now sees only boundaries - the shape of things, not colour.
    edges = cv2.Canny(blurred, 100, 200)
    describe(edges, "edges")
    cv2.imwrite(f"{OUTPUT_DIR}/5_edges.png", edges)

    edge_pixels = int(np.count_nonzero(edges))
    total_pixels = edges.shape[0] * edges.shape[1]
    print(f"\nEdge pixels found: {edge_pixels:,} "
          f"({100 * edge_pixels / total_pixels:.1f}% of the image)")

    print(f"\nAll steps saved in {OUTPUT_DIR}/ - open them and compare.")
    print("Notice how much information is thrown away at each step, and how")
    print("the shape of the objects still survives. That is the point:")
    print("the robot keeps only what it needs to make a decision.")


if __name__ == "__main__":
    main()
