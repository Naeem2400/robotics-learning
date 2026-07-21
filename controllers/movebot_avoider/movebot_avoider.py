"""
AI Robotics Bootcamp - Lesson 26
Obstacle Avoidance Robot - MoveBot learns to think.

In Lesson 25 the robot was blind: it drove for a fixed number of seconds and
had no idea what was in front of it. Now it reads its distance sensors and
decides for itself.

This is a FINITE STATE MACHINE with two states:

    MOVING   - drive forward until a sensor sees something close
    TURNING  - rotate away until the path is clear again

The e-puck has 8 infrared proximity sensors named ps0..ps7 arranged around
its body. ps0 and ps7 face forward.

        ps7   ps0
          \\   /
    ps6 --( ROBOT )-- ps1
          /       \\
        ps5       ps2

IMPORTANT: on these IR sensors a BIGGER number means something is CLOSER.
That is the opposite of a lidar, which reports distance in metres. Always
check which way your sensor works before writing the comparison.

Open worlds/movebot_avoid.wbt in Webots and press Run.
"""

from controller import Robot

TIME_STEP = 64
SPEED = 4.0

# IR reading above this = an obstacle is close enough to act on.
# Not chosen at random: e-puck sensors read roughly 0 in open space and
# climb into the hundreds as a wall gets near.
OBSTACLE_THRESHOLD = 80.0

# Must drop below this before we drive forward again. Using a LOWER value
# than the trigger prevents the robot flickering between the two states at
# the boundary - this gap is called hysteresis.
CLEAR_THRESHOLD = 60.0


def main():
    robot = Robot()

    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")
    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    # --- enable all 8 proximity sensors ---
    # Forgetting enable() is the classic bug: getValue() then returns 0
    # forever and the robot drives happily into walls.
    sensors = []
    for i in range(8):
        sensor = robot.getDevice(f"ps{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)

    state = "MOVING"
    last_state = None
    turn_direction = 1        # +1 turns right, -1 turns left

    while robot.step(TIME_STEP) != -1:
        # ---- SENSE ----------------------------------------------------
        values = [s.getValue() for s in sensors]

        front = max(values[0], values[7])       # straight ahead
        front_right = max(values[1], values[2])  # right shoulder
        front_left = max(values[5], values[6])   # left shoulder

        obstacle = max(front, front_right, front_left)

        # ---- THINK ----------------------------------------------------
        if state == "MOVING":
            if obstacle > OBSTACLE_THRESHOLD:
                # Turn away from whichever side is more blocked.
                turn_direction = -1 if front_right > front_left else 1
                state = "TURNING"

        elif state == "TURNING":
            if obstacle < CLEAR_THRESHOLD:
                state = "MOVING"

        # ---- ACT ------------------------------------------------------
        if state == "MOVING":
            left_speed = SPEED
            right_speed = SPEED
        else:                                   # TURNING - spin in place
            left_speed = SPEED * 0.5 * turn_direction
            right_speed = -SPEED * 0.5 * turn_direction

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

        # Print only when the state changes, so the console stays readable.
        if state != last_state:
            side = "right" if turn_direction > 0 else "left"
            detail = f"turning {side}" if state == "TURNING" else "path clear"
            print(f"[{robot.getTime():6.2f}s] {state:<8} "
                  f"(sensor {obstacle:6.1f}) {detail}")
            last_state = state


if __name__ == "__main__":
    main()
