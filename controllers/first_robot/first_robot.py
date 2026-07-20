"""
AI Robotics Bootcamp - Lesson 9
First Webots controller: Forward -> Stop -> Turn left -> Forward

Written for the e-puck robot, whose wheel motors are named
"left wheel motor" and "right wheel motor".

This file must live in a folder with the same name as the file:
    controllers/first_robot/first_robot.py
Webots will not find the controller otherwise.

Run it from inside Webots (set the robot's `controller` field to
"first_robot"), not with python3 from the terminal - the `controller`
module is provided by Webots itself.
"""

from controller import Robot

MAX_SPEED = 6.28   # e-puck maximum wheel speed, in radians per second

# The movement plan: (label, duration in seconds, left speed, right speed)
# Speeds are a fraction of MAX_SPEED, so 0.5 means half speed.
PLAN = [
    ("Forward",   3.0,  0.5,  0.5),
    ("Stop",      1.0,  0.0,  0.0),
    ("Turn left", 1.5, -0.3,  0.3),   # wheels spin opposite ways -> rotate
    ("Forward",   3.0,  0.5,  0.5),
    ("Stop",      0.0,  0.0,  0.0),   # final resting state
]


def setup_motors(robot):
    """Put both wheel motors into velocity mode, stopped."""
    left = robot.getDevice("left wheel motor")
    right = robot.getDevice("right wheel motor")

    # Infinite position = velocity control mode. Without this the motor
    # tries to hold a position and setVelocity will not spin it freely.
    left.setPosition(float("inf"))
    right.setPosition(float("inf"))

    left.setVelocity(0.0)
    right.setVelocity(0.0)

    return left, right


def main():
    robot = Robot()

    # The simulation advances in fixed steps. Every controller must use
    # the world's timestep so the robot stays in sync with the physics.
    timestep = int(robot.getBasicTimeStep())

    left, right = setup_motors(robot)

    step_index = 0
    step_started_at = robot.getTime()
    current_label = None

    while robot.step(timestep) != -1:
        if step_index >= len(PLAN):
            break

        label, duration, left_ratio, right_ratio = PLAN[step_index]

        # Print each phase once, as it begins.
        if label != current_label:
            print(f"[{robot.getTime():5.2f}s] {label}")
            current_label = label

        left.setVelocity(left_ratio * MAX_SPEED)
        right.setVelocity(right_ratio * MAX_SPEED)

        # Move to the next phase once this one has run long enough.
        if robot.getTime() - step_started_at >= duration:
            step_index += 1
            step_started_at = robot.getTime()

    # Always leave the robot stopped.
    left.setVelocity(0.0)
    right.setVelocity(0.0)
    print("Plan complete. Robot stopped.")


if __name__ == "__main__":
    main()
