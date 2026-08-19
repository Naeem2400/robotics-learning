"""
AI Robotics Bootcamp - Lesson 46
Autonomous hallway robot: forward, detect, turn toward the open side, continue.

Lesson 45 stopped at the wall. This controller keeps going.

    SENSE  - LDS-01 lidar → front, left, right (metres)
    THINK  - if front is blocked, turn toward whichever side is more open
    ACT    - two wheel motors (differential drive)

This is rule-based autonomy, not AI. Same Sense→Think→Act loop as Lesson 10,
now with a turn. Do not run this file with python3 — Webots provides
`controller`. Open worlds/slam_avoid.wbt and press Run.
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lidar_scan import (  # noqa: E402
    CLEAR_DISTANCE,
    STOP_DISTANCE,
    choose_turn,
    front_left_right,
)
from controller import Robot

MAX_SPEED = 3.5
TURN_SPEED = 2.2


def set_wheels(left, right, left_ratio, right_ratio):
    left.setVelocity(left_ratio * MAX_SPEED)
    right.setVelocity(right_ratio * MAX_SPEED)


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
    print("  Lesson 46 - autonomous robot")
    print(f"  FORWARD until front <= {STOP_DISTANCE:.1f} m,")
    print(f"  then TURN toward the more open side until front > {CLEAR_DISTANCE:.1f} m.")
    print("=" * 62)
    print()

    state = "FORWARD"
    turn = "LEFT"
    last = None

    while robot.step(timestep) != -1:
        ranges = list(lidar.getRangeImage())
        if not ranges:
            continue

        front, left_d, right_d = front_left_right(ranges)

        # THINK
        if state == "FORWARD":
            if front <= STOP_DISTANCE:
                turn = choose_turn(left_d, right_d)
                state = "TURNING"
        elif state == "TURNING":
            if front > CLEAR_DISTANCE:
                state = "FORWARD"

        # ACT — differential drive
        #   both +          → forward
        #   left -, right + → spin left  (counter-clockwise)
        #   left +, right - → spin right (clockwise)
        if state == "FORWARD":
            set_wheels(left, right, 1.0, 1.0)
        elif turn == "LEFT":
            set_wheels(left, right, -TURN_SPEED / MAX_SPEED, TURN_SPEED / MAX_SPEED)
        else:
            set_wheels(left, right, TURN_SPEED / MAX_SPEED, -TURN_SPEED / MAX_SPEED)

        if state != last:
            shown = "clear" if front == float("inf") else f"{front:.2f} m"
            extra = f" toward {turn}  (L {left_d:.2f}  R {right_d:.2f})" if state == "TURNING" else ""
            print(f"[{robot.getTime():6.2f}s] {state:<8}  front {shown}{extra}")
            last = state


if __name__ == "__main__":
    main()
