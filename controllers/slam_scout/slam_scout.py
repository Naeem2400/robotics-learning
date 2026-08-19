"""
AI Robotics Bootcamp - Lesson 45
SLAM scout: drive toward a wall, read the lidar, stop at one metre.

This is the first real LiDAR loop in the SLAM module. It does NOT build a
map. It does the thing a map is made of:

    SENSE  - TurtleBot3 LDS-01, 360 beams, distances in metres
    THINK  - if front <= 1.0 m then STOP, else FORWARD
    ACT    - two wheel motors

When it stops it prints one occupancy sketch from that pose - a snapshot,
not SLAM. Lesson 46 adds turning. Later lessons add odometry + mapping.

Open worlds/slam_lab.wbt in Webots and press Run.

This file is a Webots controller. Do not run it with python3 in a terminal;
the `controller` module is provided by Webots itself.
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lidar_scan import (  # noqa: E402
    STOP_DISTANCE,
    describe,
    front_left_right,
    occupancy_from_scan,
    render_grid,
    should_stop,
)
from controller import Robot

MAX_SPEED = 3.0          # rad/s - slow so the console is readable
PRINT_EVERY = 0.6        # seconds between live reports


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    left = robot.getDevice("left wheel motor")
    right = robot.getDevice("right wheel motor")
    for motor in (left, right):
        motor.setPosition(float("inf"))
        motor.setVelocity(0.0)

    lidar = robot.getDevice("LDS-01")
    lidar.enable(timestep)

    print("=" * 62)
    print("  Lesson 45 - SLAM scout")
    print("  Drive forward. Stop when the wall is closer than "
          f"{STOP_DISTANCE:.1f} m.")
    print("=" * 62)
    print()

    next_report = 0.0
    stopped = False

    while robot.step(timestep) != -1:
        ranges = list(lidar.getRangeImage())
        if not ranges:
            continue

        report = describe(ranges)
        front, _, _ = front_left_right(ranges)

        if should_stop(front):
            left.setVelocity(0.0)
            right.setVelocity(0.0)
            if not stopped:
                print(f"[{robot.getTime():6.2f}s]")
                print(report)
                print()
                print("  Occupancy sketch from this pose (not a map yet):")
                print()
                print(render_grid(occupancy_from_scan(ranges)))
                print()
                print("  Wall reached. This is the measurement SLAM will")
                print("  accumulate. Lesson 46: turn and keep going.")
                stopped = True
            continue

        left.setVelocity(MAX_SPEED)
        right.setVelocity(MAX_SPEED)

        now = robot.getTime()
        if now >= next_report:
            print(f"[{now:6.2f}s] {report.splitlines()[0].strip()}")
            print(f"            {report.splitlines()[-1].strip()}")
            next_report = now + PRINT_EVERY


if __name__ == "__main__":
    main()
