"""
AI Robotics Bootcamp - Lesson 25
MoveBot: your first robot in Webots.

This is the homework sequence, solved:

    5 seconds forward  ->  left turn  ->  5 seconds forward  ->  stop

It shows TIME-BASED movement: the robot does not know where it is, it only
knows how long it has been doing something. That is the simplest form of
robot control, and the starting point for everything else.

Open worlds/movebot.wbt in Webots and press Run.
"""

from controller import Robot

TIME_STEP = 64        # the simulation updates every 64 milliseconds
SPEED = 4.0           # rad/s - a comfortable cruising speed for the e-puck

# Each step: (label, how many seconds, left speed, right speed)
#
#   both wheels equal      -> straight
#   left slower than right -> curves left
#   left faster than right -> curves right
#   opposite signs         -> spins on the spot
SEQUENCE = [
    ("Forward",   5.0,  SPEED,       SPEED),
    ("Left turn", 1.6,  SPEED * 0.5, SPEED * 1.5),
    ("Forward",   5.0,  SPEED,       SPEED),
    ("Stop",      0.0,  0.0,         0.0),
]


def main():
    robot = Robot()

    # --- get the two wheel motors out of the robot ---
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    # Infinite position = velocity control. Without this the motor tries to
    # hold a fixed angle and setVelocity will not spin the wheel freely.
    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))

    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    step_index = 0
    step_started = 0.0
    current_label = None

    # --- the control loop: every robot has one ---
    while robot.step(TIME_STEP) != -1:
        now = robot.getTime()

        if step_index >= len(SEQUENCE):
            break

        label, duration, left_speed, right_speed = SEQUENCE[step_index]

        # Announce each phase once, as it starts.
        if label != current_label:
            print(f"[{now:5.2f}s] {label}")
            current_label = label

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

        # Move to the next phase once this one has run long enough.
        if now - step_started >= duration:
            step_index += 1
            step_started = now

    # Always leave the robot stopped.
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    print("Sequence complete. MoveBot stopped.")


if __name__ == "__main__":
    main()
