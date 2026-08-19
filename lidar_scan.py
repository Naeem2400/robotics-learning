"""
AI Robotics Bootcamp - Lesson 45
LiDAR scan math: one sweep of ranges becomes a decision and a sketch.

This is the step BEFORE SLAM. A lidar does not build a map by itself. It
returns a list of distances. This file turns that list into:

  1. front / left / right  - what the robot uses to decide
  2. should_stop()         - the one-metre rule
  3. a polar printout      - so you can SEE the scan
  4. a tiny occupancy grid - one snapshot of the room, from one pose

The Webots controller (controllers/slam_scout/slam_scout.py) calls the same
functions on a live TurtleBot3. This file needs no Webots, so CI and the
notebook can run it.

Usage:
    python3 lidar_scan.py --test
    python3 lidar_scan.py --demo
"""

from __future__ import annotations

import argparse
import math


STOP_DISTANCE = 1.0     # metres - the rule from the lesson
CLEAR_DISTANCE = 1.3    # metres - stay turning until front is this clear
SCAN_METRES = 3.5       # occupancy sketch saturates at this range


def safe_min(beams):
    """Smallest valid distance. 0 and inf are 'no echo', not 'touching'."""
    valid = [d for d in beams if d > 0.0 and d != float("inf")]
    return min(valid) if valid else float("inf")


def front_left_right(ranges):
    """Split a 360-beam scan into three cones. Middle of the list is forward.

    The TurtleBot3 LDS-01 in Webots returns one reading per degree. The same
    slicing is used in Lesson 12's sensor_explorer.
    """
    n = len(ranges)
    if n < 16:
        raise ValueError("need a full lidar sweep, not a single beam")
    centre = n // 2
    cone = n // 8
    front = safe_min(ranges[centre - cone:centre + cone])
    left = safe_min(ranges[centre + cone:centre + 3 * cone])
    right = safe_min(ranges[centre - 3 * cone:centre - cone])
    return front, left, right


def should_stop(front, threshold=STOP_DISTANCE):
    """Rule-based robotics: closer than the threshold means STOP.

    This is not AI and it is not SLAM. It is the foundation both sit on.
    A lidar reports metres, so SMALLER = closer. (IR proximity sensors in
    Lesson 26 work the opposite way.)
    """
    return front <= threshold


def choose_turn(left, right):
    """Pick the more open side. LEFT if left >= right, otherwise RIGHT."""
    return "LEFT" if left >= right else "RIGHT"


def choose_action(front, left, right, threshold=STOP_DISTANCE):
    """One Sense→Think step: FORWARD, or turn toward the clearer side."""
    if front > threshold:
        return "FORWARD"
    return "TURN_" + choose_turn(left, right)


def fake_corridor(n=360, front=2.4, left=1.2, right=0.8, back=8.0):
    """A synthetic hallway scan so --test does not need Webots."""
    ranges = [float(back)] * n
    centre = n // 2
    cone = n // 8
    for i in range(centre - cone, centre + cone):
        ranges[i] = float(front)
    for i in range(centre + cone, centre + 3 * cone):
        ranges[i] = float(left)
    for i in range(centre - 3 * cone, centre - cone):
        ranges[i] = float(right)
    return ranges


def render_polar(ranges, ticks=36):
    """Downsample a 360-beam sweep into a one-line polar sketch."""
    n = len(ranges)
    step = max(n // ticks, 1)
    chars = []
    for i in range(0, n, step):
        d = safe_min(ranges[i:i + step])
        if d == float("inf") or d >= 3.0:
            chars.append(".")
        elif d >= 1.5:
            chars.append("o")
        else:
            chars.append("#")
    return "".join(chars)


def occupancy_from_scan(ranges, size=17, metres=SCAN_METRES):
    """Project one lidar sweep onto a bird's-eye grid. Robot is the centre.

    This is NOT SLAM. SLAM needs many scans from many poses, plus odometry.
    One scan from one pose is a snapshot - the 'environment representation'
    the lesson asks for before we add mapping.
    """
    grid = [[" "] * size for _ in range(size)]
    cx = cy = size // 2
    grid[cy][cx] = "R"
    n = len(ranges)
    radius = size // 2
    for i, distance in enumerate(ranges):
        if distance <= 0 or distance == float("inf") or distance > metres:
            continue
        # i == n/2 is forward (+x). Positive angle is the robot's left (+y).
        angle = (i - n / 2.0) * (2.0 * math.pi / n)
        gx = cx + int(round((distance / metres) * radius * math.cos(angle)))
        gy = cy - int(round((distance / metres) * radius * math.sin(angle)))
        if 0 <= gx < size and 0 <= gy < size and grid[gy][gx] != "R":
            grid[gy][gx] = "#"
    return grid


def render_grid(grid):
    return "\n".join("    " + "".join(row) for row in grid)


def describe(ranges, threshold=STOP_DISTANCE):
    """Human-readable report for one scan."""
    front, left, right = front_left_right(ranges)
    lines = [
        f"  FRONT {front:5.2f} m    LEFT {left:5.2f} m    RIGHT {right:5.2f} m",
        f"  polar {render_polar(ranges)}",
    ]
    if should_stop(front, threshold):
        lines.append(f"  decision: STOP  (front {front:.2f} m <= {threshold:.1f} m)")
    else:
        lines.append(f"  decision: FORWARD  (front {front:.2f} m > {threshold:.1f} m)")
    return "\n".join(lines)


def run_test():
    far = fake_corridor(front=2.4, left=1.2, right=0.8)
    front, left, right = front_left_right(far)
    assert abs(front - 2.4) < 1e-9
    assert abs(left - 1.2) < 1e-9
    assert abs(right - 0.8) < 1e-9
    assert should_stop(front) is False

    near = fake_corridor(front=0.7, left=1.2, right=0.8)
    assert should_stop(front_left_right(near)[0]) is True
    assert choose_action(0.5, 2.0, 0.8) == "TURN_LEFT"
    assert choose_action(0.5, 0.8, 2.0) == "TURN_RIGHT"
    assert choose_action(2.4, 1.2, 0.8) == "FORWARD"

    grid = occupancy_from_scan(far)
    assert grid[len(grid) // 2][len(grid) // 2] == "R"
    assert any("#" in row for row in grid)

    print("  Lesson 45 tests passed.")
    print("  A lidar scan splits into front/left/right, STOP is the one-metre")
    print("  rule, and one sweep already sketches a room — that is not SLAM")
    print("  yet, it is the measurement SLAM will accumulate.")
    print()
    print("  Next: open worlds/slam_lab.wbt in Webots and press Run.")


def run_demo():
    print("=" * 62)
    print("  Lesson 45 - one lidar scan of a hallway (no Webots needed)")
    print("=" * 62)
    print()
    for metres in (5.0, 4.0, 3.0, 2.0, 1.0, 0.7):
        scan = fake_corridor(front=metres, left=1.2, right=0.8)
        print(f"  wall {metres:.1f} m ahead")
        print(describe(scan))
        print()
    print("  Occupancy sketch at 2.4 m (R = robot, # = hit):")
    print()
    print(render_grid(occupancy_from_scan(fake_corridor())))
    print()


def main():
    parser = argparse.ArgumentParser(description="Lesson 45 — lidar scan math")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.test:
        run_test()
        return
    run_demo()


if __name__ == "__main__":
    main()
