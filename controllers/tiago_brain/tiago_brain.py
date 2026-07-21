"""
AI Robotics Bootcamp - Lesson 10 (TIAGo version)
The robot's brain on a human-scale service robot exploring a room.

Same Sense -> Think -> Act idea as robot_brain.py, but now with a real
laser scanner and robust obstacle avoidance so the robot never wedges:

  SENSE : a lidar measures distance to furniture and walls
  THINK : a small state machine decides FORWARD / TURN / BACK
  ACT   : the two drive wheels move the robot

States:
  FORWARD - drive ahead until something is within TURN_DISTANCE
  TURN    - rotate in place (toward the more open side) until the way
            ahead is clear by a comfortable margin
  BACK    - if wedged very close, reverse briefly, then try turning the
            other way. This is what stops it getting stuck.

Run it from inside Webots: open worlds/tiago_room.wbt and press Run.
"""

from controller import Robot

MAX_SPEED = 6.0          # rad/s (TIAGo wheels allow up to 10.15)
TURN_DISTANCE = 1.0      # start turning early - TIAGo is wide, keep clearance (m)
CLEAR_DISTANCE = 1.3     # drive forward again once this clear ahead (m)
WEDGED_DISTANCE = 0.35   # closer than this = stuck, back up
STUCK_LIMIT = 70         # turning this many steps with no luck = back up
BACK_STEPS = 20          # how long to reverse when wedged
BATTERY_DRAIN = 0.005    # very slow drain so it roams a long time first


def safe_min(beams):
    """Smallest valid distance in a set of lidar beams (ignore 0 and inf)."""
    valid = [d for d in beams if d > 0.0 and d != float("inf")]
    return min(valid) if valid else float("inf")


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    left = robot.getDevice("wheel_left_joint")
    right = robot.getDevice("wheel_right_joint")
    for motor in (left, right):
        motor.setPosition(float("inf"))
        motor.setVelocity(0.0)

    lidar = robot.getDevice("Hokuyo URG-04LX-UG01")
    lidar.enable(timestep)

    battery = 100.0
    state = "FORWARD"
    turn_dir = 1            # +1 or -1: which way we rotate
    turn_steps = 0
    back_steps = 0
    last_state = None

    while robot.step(timestep) != -1:
        # 1. SENSE -------------------------------------------------------
        ranges = lidar.getRangeImage()
        n = len(ranges)
        c = n // 2
        fspan = n // 12                                       # narrow ~15 deg cone
        front = safe_min(ranges[c - fspan:c + fspan])         # straight ahead only
        left_side = safe_min(ranges[c + fspan:c + n // 3])    # open space left?
        right_side = safe_min(ranges[c - n // 3:c - fspan])   # open space right?

        battery -= BATTERY_DRAIN

        # 2. THINK (safety overrides first, then the avoidance state machine)
        if battery < 20:
            state = "CHARGE"
        elif state == "FORWARD":
            if front < TURN_DISTANCE:
                # Turn toward whichever side has more room.
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
                turn_dir = -turn_dir      # try the other way this time
                state = "TURN"
                turn_steps = 0

        # 3. ACT ---------------------------------------------------------
        if state == "FORWARD":
            ls, rs = 0.6, 0.6
        elif state == "TURN":
            ls, rs = 0.5 * turn_dir, -0.5 * turn_dir
        elif state == "BACK":
            ls, rs = -0.4, -0.4
        else:                              # CHARGE -> stop
            ls, rs = 0.0, 0.0

        left.setVelocity(ls * MAX_SPEED)
        right.setVelocity(rs * MAX_SPEED)

        # Print only on state change, with the front distance.
        if state != last_state:
            shown = "clear" if front == float("inf") else f"{front:.2f} m"
            print(f"[battery {battery:5.1f}%] {state:<8} (front: {shown})")
            last_state = state


if __name__ == "__main__":
    main()
