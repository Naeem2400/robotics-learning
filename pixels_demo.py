"""
AI Robotics Bootcamp - Lesson 13
An image is just numbers.

This script proves the central idea of the lesson without any libraries:
it builds a small image out of raw numbers, prints those numbers, converts
the colour image to grayscale by hand, and saves both as real PNG files
you can open.

Run with:
    python3 pixels_demo.py
"""

import struct
import zlib

WIDTH = 16
HEIGHT = 16


# ---------------------------------------------------------------------------
# Making an image out of numbers
# ---------------------------------------------------------------------------

def build_image(width, height):
    """Build a colour image as a grid of (red, green, blue) numbers.

    Every pixel is just three numbers from 0 to 255. That is all an image is.
    Here red increases to the right and green increases downwards, with a
    blue square in the middle.
    """
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            red = int(255 * x / (width - 1))
            green = int(255 * y / (height - 1))
            blue = 255 if (4 <= x < 12 and 4 <= y < 12) else 40
            row.append((red, green, blue))
        rows.append(row)
    return rows


def to_grayscale(rows):
    """Convert colour to grayscale: one brightness number per pixel.

    The human eye is most sensitive to green and least to blue, so the
    standard formula weights them differently instead of a plain average.
    """
    gray_rows = []
    for row in rows:
        gray_rows.append([
            int(0.299 * r + 0.587 * g + 0.114 * b) for (r, g, b) in row
        ])
    return gray_rows


# ---------------------------------------------------------------------------
# Showing the numbers
# ---------------------------------------------------------------------------

def show_pixel_values(rows):
    """Print the actual numbers behind a few pixels."""
    print("A few individual pixels (red, green, blue):")
    for (x, y) in [(0, 0), (8, 8), (15, 0), (15, 15)]:
        r, g, b = rows[y][x]
        print(f"  pixel at x={x:<3} y={y:<3} -> R={r:<4} G={g:<4} B={b}")
    print()


def show_ascii(gray_rows):
    """Draw the grayscale image using characters, dark to light."""
    shades = " .:-=+*#%@"
    print("The same image drawn as characters (dark -> light):")
    for row in gray_rows:
        line = "".join(shades[min(v * len(shades) // 256, len(shades) - 1)]
                       for v in row)
        print("  " + line)
    print()


# ---------------------------------------------------------------------------
# Saving a real PNG (standard library only)
# ---------------------------------------------------------------------------

def write_png(path, rows):
    """Write a list of RGB rows to a real .png file."""
    height = len(rows)
    width = len(rows[0])

    raw = b""
    for row in rows:
        raw += b"\x00"                       # filter byte for this scanline
        raw += bytes(value for pixel in row for value in pixel)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw))
    png += chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(png)


def main():
    print("=" * 58)
    print("  Lesson 13 - An image is just numbers")
    print("=" * 58)

    colour = build_image(WIDTH, HEIGHT)

    total = WIDTH * HEIGHT
    print(f"Resolution : {WIDTH} x {HEIGHT}")
    print(f"Pixels     : {total:,}")
    print(f"Numbers    : {total * 3:,}  (3 per pixel: red, green, blue)")
    print()

    show_pixel_values(colour)

    gray = to_grayscale(colour)
    show_ascii(gray)

    # Save both versions. Grayscale is written back out as RGB so the same
    # PNG writer can handle it - each pixel just has R = G = B.
    gray_as_rgb = [[(v, v, v) for v in row] for row in gray]
    write_png("output_colour.png", colour)
    write_png("output_gray.png", gray_as_rgb)

    print("Saved output_colour.png and output_gray.png - open them and look.")
    print()
    print("Why grayscale matters: colour needs 3 numbers per pixel, grayscale")
    print(f"needs 1. That is {total * 3:,} numbers vs {total:,} - three times")
    print("less work for the robot. This is why many vision steps drop colour.")


if __name__ == "__main__":
    main()
