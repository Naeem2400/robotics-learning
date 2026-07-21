"""
AI Robotics Bootcamp - Lesson 27
SLAM: build a map of an unknown room, and see why localization matters.

The script runs the same robot through the same room twice:

  PASS 1 - the robot knows exactly where it is  -> a clean map
  PASS 2 - its position estimate slowly drifts  -> a ruined map

Pass 2 is the important one. It shows why you cannot simply "do mapping":
a map built from a wrong position is worse than no map at all. Solving both
problems at once is what the S in SLAM means.

Needs no libraries.

Run with:
    python3 slam_demo.py
"""

import math

# The real room. The robot never gets to see this - it must discover it.
#   '#' = wall or obstacle,  '.' = free space
TRUE_MAP = [
    "########################################",
    "#......................................#",
    "#....########..........................#",
    "#....#......#..............######......#",
    "#....#......#..............#....#......#",
    "#....########..............#....#......#",
    "#..........................######......#",
    "#......................................#",
    "#...............########...............#",
    "#...............#......#...............#",
    "#...............########...............#",
    "#......................................#",
    "########################################",
]

HEIGHT = len(TRUE_MAP)
WIDTH = len(TRUE_MAP[0])

# Where the robot drives. It follows these waypoints in order.
PATH = [(4, 7), (20, 7), (34, 3), (34, 10), (20, 11), (6, 11), (4, 7)]

NUM_BEAMS = 90          # lidar beams per scan
MAX_RANGE = 14.0        # how far the lidar can see, in cells
DRIFT_PER_STEP = 0.045  # how fast the position estimate goes wrong in pass 2

UNKNOWN, FREE, OCCUPIED = 0, 1, 2


def is_wall(x, y):
    """Is this cell solid in the real room?"""
    ix, iy = int(round(x)), int(round(y))
    if not (0 <= ix < WIDTH and 0 <= iy < HEIGHT):
        return True
    return TRUE_MAP[iy][ix] == "#"


def cast_ray(true_x, true_y, angle):
    """Walk one laser beam outward until it hits something.

    Returns the distance travelled. This is the physics of a lidar: it always
    measures from where the robot REALLY is.
    """
    distance = 0.0
    while distance < MAX_RANGE:
        distance += 0.25
        x = true_x + math.cos(angle) * distance
        y = true_y + math.sin(angle) * distance
        if is_wall(x, y):
            return distance
    return MAX_RANGE


def integrate_scan(grid, believed_x, believed_y, readings):
    """Write one scan into the map, from where the robot THINKS it is.

    This is the crux of the whole demo. The measurements are real, but they
    are recorded relative to the believed position. If that belief is wrong,
    correct measurements get written into the wrong cells.
    """
    for angle, distance in readings:
        # Mark everything along the beam as free space.
        step = 0.0
        while step < distance - 0.5:
            step += 0.5
            x = int(round(believed_x + math.cos(angle) * step))
            y = int(round(believed_y + math.sin(angle) * step))
            if 0 <= x < WIDTH and 0 <= y < HEIGHT and grid[y][x] == UNKNOWN:
                grid[y][x] = FREE

        # If the beam stopped short of its maximum, it hit something.
        if distance < MAX_RANGE:
            x = int(round(believed_x + math.cos(angle) * distance))
            y = int(round(believed_y + math.sin(angle) * distance))
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                grid[y][x] = OCCUPIED


def walk_path():
    """Yield (x, y) positions along the waypoint path."""
    for i in range(len(PATH) - 1):
        x1, y1 = PATH[i]
        x2, y2 = PATH[i + 1]
        steps = int(max(abs(x2 - x1), abs(y2 - y1)))
        for s in range(steps):
            t = s / max(steps, 1)
            yield x1 + (x2 - x1) * t, y1 + (y2 - y1) * t


def run(drift=False):
    """Drive the robot around the room once, building a map as it goes."""
    grid = [[UNKNOWN] * WIDTH for _ in range(HEIGHT)]

    drift_x = drift_y = 0.0

    for true_x, true_y in walk_path():
        if drift:
            # Odometry error accumulates - wheels slip, encoders round off.
            # Nothing corrects it, so the error only ever grows.
            drift_x += DRIFT_PER_STEP
            drift_y += DRIFT_PER_STEP * 0.35

        believed_x = true_x + drift_x
        believed_y = true_y + drift_y

        readings = []
        for b in range(NUM_BEAMS):
            angle = 2 * math.pi * b / NUM_BEAMS
            readings.append((angle, cast_ray(true_x, true_y, angle)))

        integrate_scan(grid, believed_x, believed_y, readings)

    return grid, drift_x, drift_y


def render(grid, title):
    symbols = {UNKNOWN: " ", FREE: ".", OCCUPIED: "#"}
    print(f"  {title}")
    for row in grid:
        print("    " + "".join(symbols[cell] for cell in row))
    print()


def accuracy(grid):
    """How many discovered cells match the real room?"""
    checked = correct = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == UNKNOWN:
                continue
            checked += 1
            actually_wall = TRUE_MAP[y][x] == "#"
            thinks_wall = grid[y][x] == OCCUPIED
            if actually_wall == thinks_wall:
                correct += 1
    return (100.0 * correct / checked) if checked else 0.0, checked


def main():
    print("=" * 62)
    print("  Lesson 27 - SLAM: mapping an unknown room")
    print("=" * 62)
    print()
    print("  The real room (the robot cannot see this):")
    print()
    for row in TRUE_MAP:
        print("    " + row)
    print()

    print("-" * 62)
    print("  PASS 1: the robot knows exactly where it is")
    print("-" * 62)
    clean, _, _ = run(drift=False)
    render(clean, "The map it built:")
    clean_score, clean_cells = accuracy(clean)
    print(f"    {clean_cells} cells discovered, {clean_score:.1f}% correct\n")

    print("-" * 62)
    print("  PASS 2: the same robot, but its position slowly drifts")
    print("-" * 62)
    drifted, dx, dy = run(drift=True)
    render(drifted, "The map it built:")
    drift_score, drift_cells = accuracy(drifted)
    print(f"    {drift_cells} cells discovered, {drift_score:.1f}% correct")
    print(f"    final position error: {math.hypot(dx, dy):.1f} cells\n")

    print("=" * 62)
    print("  Why this matters")
    print("=" * 62)
    print()
    print(f"  Same room. Same sensor. Same path. Accuracy fell from")
    print(f"  {clean_score:.1f}% to {drift_score:.1f}% - the walls smear and")
    print("  double up, because correct measurements were written into the")
    print("  wrong cells.")
    print()
    print("  The lidar was never wrong. The POSITION was.")
    print()
    print("  This is why mapping and localization cannot be solved")
    print("  separately - each one needs the other to be correct.")
    print("  Solving both at the same time is what SLAM means.")


if __name__ == "__main__":
    main()
