"""
AI Robotics Bootcamp - Lesson 29
Why AI vision replaced hand-written rules.

Traditional computer vision means a programmer writes the rules:

    if the pixel is red -> it is an apple

That works beautifully on the picture you tested with. This script shows
what happens on the next five pictures.

Needs no libraries.

Run with:
    python3 traditional_vs_ai_vision.py
"""

WIDTH, HEIGHT = 24, 12


# ---------------------------------------------------------------------------
# Making test images (each is a grid of (r, g, b) pixels)
# ---------------------------------------------------------------------------

def make_image(object_colour, background=(240, 240, 235), brightness=1.0):
    """Draw a blob of object_colour on a background, at a given brightness."""

    def dim(colour):
        return tuple(int(c * brightness) for c in colour)

    rows = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # An oval blob in the middle of the frame.
            inside = ((x - 12) / 5.0) ** 2 + ((y - 6) / 3.5) ** 2 <= 1.0
            row.append(dim(object_colour) if inside else dim(background))
        rows.append(row)
    return rows


# The rule-based detector's idea of "red".
def looks_red(pixel):
    r, g, b = pixel
    return r > 200 and g < 80 and b < 80


def rule_based_detector(image):
    """Traditional computer vision: count pixels matching a hand-written rule."""
    matches = sum(1 for row in image for pixel in row if looks_red(pixel))
    total = WIDTH * HEIGHT
    # If enough of the frame is "red", call it an apple.
    return matches > total * 0.08, matches


def show(image, label):
    print(f"  {label}")
    for row in image:
        line = "".join("##" if looks_red(p) else ".." for p in row)
        print("    " + line)


# ---------------------------------------------------------------------------

RED_APPLE = (230, 40, 40)
GREEN_APPLE = (110, 180, 70)
RED_BALL = (230, 40, 40)

TESTS = [
    # (description, image, is it really an apple?)
    ("A red apple, good lighting",
     make_image(RED_APPLE), True),

    ("The same apple, dim evening light",
     make_image(RED_APPLE, brightness=0.55), True),

    ("The same apple, in shadow",
     make_image(RED_APPLE, brightness=0.35), True),

    ("A GREEN apple",
     make_image(GREEN_APPLE), True),

    ("A red rubber BALL (not an apple)",
     make_image(RED_BALL), False),
]


def main():
    print("=" * 62)
    print("  Lesson 29 - Rule-based vision vs AI vision")
    print("=" * 62)
    print()
    print("  The rule a programmer wrote:")
    print("      if r > 200 and g < 80 and b < 80  ->  it is an apple")
    print()
    print("  '##' marks pixels the rule accepted as red.")
    print()

    correct = 0

    for description, image, truly_apple in TESTS:
        print("-" * 62)
        detected, matched = rule_based_detector(image)
        show(image, description)

        verdict = "APPLE" if detected else "no apple"
        truth = "an apple" if truly_apple else "NOT an apple"
        right = detected == truly_apple
        correct += right

        print(f"    rule says : {verdict}  ({matched} red pixels)")
        print(f"    reality   : it is {truth}")
        print(f"    result    : {'correct' if right else '*** WRONG ***'}")
        print()

    print("=" * 62)
    print(f"  Score: {correct} out of {len(TESTS)} correct")
    print("=" * 62)
    print()
    print("  The rule worked perfectly on the picture it was written for,")
    print("  then failed three ways:")
    print()
    print("    - dim light  : the SAME apple stopped being 'red enough'")
    print("    - shadow     : the same apple again, missed completely")
    print("    - green apple: still an apple, but not red at all")
    print("    - red ball   : not an apple, but the rule cannot tell")
    print()
    print("  You could patch each failure with another rule. Then someone")
    print("  photographs an apple at sunset, or a tomato appears, and you")
    print("  patch again. This never ends.")
    print()
    print("  An AI model is not given rules. It is shown thousands of")
    print("  labelled apples - bright, dim, red, green, partly hidden - and")
    print("  learns what they have in common. That is the whole difference,")
    print("  and it is why modern robots use trained models.")
    print()
    print("  But note: rules are NOT obsolete. If your robot only ever sees")
    print("  one factory conveyor under fixed lighting, a colour rule is")
    print("  faster, simpler, and needs no training data. Choosing between")
    print("  them is an engineering decision, not a fashion.")


if __name__ == "__main__":
    main()
