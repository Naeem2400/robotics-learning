"""
AI Robotics Bootcamp - Lesson 15
See an image the way a robot sees it.

You see a picture. The robot receives a table of numbers. This script shows
you both views of the SAME data, side by side, so the difference is obvious.

Uses no libraries at all, so it runs before OpenCV is installed.

Run with:
    python3 see_like_a_robot.py
"""

WIDTH = 12
HEIGHT = 8

BACKGROUND = (235, 235, 235)   # light grey
SHAPE = (200, 30, 30)          # a red block


def build_image():
    """Return the image as rows of (red, green, blue) pixels."""
    rows = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            inside = 3 <= x < 9 and 2 <= y < 6
            row.append(SHAPE if inside else BACKGROUND)
        rows.append(row)
    return rows


def show_as_picture(rows):
    """The human view: blocks of colour that look like a shape."""
    print("WHAT YOU SEE (a red block on a light background):\n")
    for row in rows:
        line = "".join("##" if pixel == SHAPE else ".." for pixel in row)
        print("   " + line)
    print()


def show_as_numbers(rows, max_rows=4):
    """The robot's view: the same data as raw numbers."""
    print("WHAT THE ROBOT RECEIVES (the same image, as numbers):\n")
    for y, row in enumerate(rows[:max_rows]):
        cells = " ".join(f"[{r:3},{g:3},{b:3}]" for (r, g, b) in row[:5])
        print(f"   row {y}: {cells} ...")
    print(f"   ... and {HEIGHT - max_rows} more rows\n")


def inspect_pixels(rows):
    """Read individual pixels, the way you would in OpenCV."""
    print("READING SINGLE PIXELS (note: image[y, x] - row first!):\n")
    for (x, y) in [(0, 0), (5, 3), (11, 7)]:
        r, g, b = rows[y][x]
        where = "inside the shape" if rows[y][x] == SHAPE else "background"
        print(f"   image[{y}, {x}] -> R={r:3} G={g:3} B={b:3}   ({where})")
    print()


def main():
    rows = build_image()

    print("=" * 60)
    print("  Lesson 15 - The same image, two very different views")
    print("=" * 60 + "\n")

    show_as_picture(rows)
    show_as_numbers(rows)
    inspect_pixels(rows)

    total = WIDTH * HEIGHT
    print("-" * 60)
    print(f"Image shape : ({HEIGHT}, {WIDTH}, 3)   <- height, width, channels")
    print(f"Pixels      : {total}")
    print(f"Numbers     : {total * 3}")
    print("-" * 60)
    print()
    print("There is no 'red block' anywhere in that data - only numbers.")
    print("The shape exists in YOUR head, not in the robot's memory.")
    print("A robot needs a trained model before those numbers mean anything.")


if __name__ == "__main__":
    main()
