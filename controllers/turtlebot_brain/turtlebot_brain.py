"""
AI Robotics Bootcamp - Lesson 10 (TurtleBot3 version)
A small robot exploring a big room.

Same Sense -> Think -> Act brain, on a tiny robot:
  SENSE : a 360-degree lidar (LDS-01) measures distance all around
  THINK : a state machine decides FORWARD / TURN / BACK
  ACT   : two drive wheels move the robot

The robot is only ~14 cm wide with nothing sticking out, so unlike a big
robot it can turn inside tight spaces and will not wedge on furniture.

Run it from inside Webots: open worlds/turtlebot_room.wbt and press Run.
"""

from controller import Robot

MAX_SPEED = 6.0          # rad/s (TurtleBot3 wheels allow up to 6.67)
TURN_DISTANCE = 0.40     # start turning when something is this close ahead (m)
CLEAR_DISTANCE = 0.55    # drive forward again once this clear ahead (m)
WEDGED_DISTANCE = 0.16   # closer than this = stuck, back up
STUCK_LIMIT = 70         # turning this many steps with no luck = back up
BACK_STEPS = 20          # how long to reverse when wedged
BATTERY_DRAIN = 0.005    # very slow drain so it roams a long time


def safe_min(beams):
    """Smallest valid distance in a set of lidar beams (ignore 0 and inf)."""
    valid = [d for d in beams if d > 0.0 and d != float("inf")]
    return min(valid) if valid else float("inf")


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    left = robot.getDevice("left wheel motor")
    right = robot.getDevice("right wheel motor")
    for motor in (left, right):
        motor.setPosition(float("inf"))     # velocity control mode
        motor.setVelocity(0.0)

    lidar = robot.getDevice("LDS-01")
    lidar.enable(timestep)

    battery = 100.0
    state = "FORWARD"
    turn_dir = 1
    turn_steps = 0
    back_steps = 0
    last_state = None

    while robot.step(timestep) != -1:
        # 1. SENSE -------------------------------------------------------
        # The LDS-01 gives 360 beams (one per degree). The middle of the
        # list points straight ahead.
        ranges = lidar.getRangeImage()
        n = len(ranges)
        c = n // 2
        fspan = n // 18                                       # ~20 deg cone
        front = safe_min(ranges[c - fspan:c + fspan])
        left_side = safe_min(ranges[c + fspan:c + n // 4])
        right_side = safe_min(ranges[c - n // 4:c - fspan])

        battery -= BATTERY_DRAIN

        # 2. THINK -------------------------------------------------------
        if battery < 20:
            state = "CHARGE"
        elif state == "FORWARD":
            if front < TURN_DISTANCE:
                turn_dir = 1 if right_side >= left_side else -1
                state = "TURN"
                turn_steps = 0
        elif state == "TURN":
            turn_steps += 1
            if front > CLEAR_DISTANCE:
                state = "FORWARD"
            elif front < WEDGED_DISTANCE or turn_steps > STUCK_LIMIT:
                state = "BACK"
                back_steps = BACK_STEPS
        elif state == "BACK":
            back_steps -= 1
            if back_steps <= 0:
                turn_dir = -turn_dir
                state = "TURN"
                turn_steps = 0

        # 3. ACT ---------------------------------------------------------
        if state == "FORWARD":
            ls, rs = 0.9, 0.9
        elif state == "TURN":
            ls, rs = 0.6 * turn_dir, -0.6 * turn_dir
        elif state == "BACK":
            ls, rs = -0.5, -0.5
        else:                                # CHARGE -> stop
            ls, rs = 0.0, 0.0

        left.setVelocity(ls * MAX_SPEED)
        right.setVelocity(rs * MAX_SPEED)

        if state != last_state:
            shown = "clear" if front == float("inf") else f"{front:.2f} m"
            print(f"[battery {battery:5.1f}%] {state:<8} (front: {shown})")
            last_state = state


if __name__ == "__main__":
    main()
