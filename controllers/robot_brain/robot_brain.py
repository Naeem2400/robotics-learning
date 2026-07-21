"""
AI Robotics Bootcamp - Lesson 10 (Webots version)
The robot's brain running on a REAL simulated robot.

This is robot_brain.py brought to life: instead of hard-coded numbers,
the e-puck reads its own distance sensors every step and decides what to do.

    SENSE  -> read the 8 proximity sensors
    THINK  -> decide() picks an action
    ACT    -> drive the motors

Run it from inside Webots by opening worlds/brain_robot.wbt and pressing Run.
"""

from controller import Robot

MAX_SPEED = 6.28          # e-puck top wheel speed (rad/s)
OBSTACLE_LEVEL = 80.0     # proximity reading above this = something is close
BATTERY_DRAIN = 0.03      # how fast the (pretend) battery falls each step


def decide(front_obstacle, battery, human_detected=False):
    """The brain. Same priority order as the terminal version:
    human safety first, then battery, then obstacles, then move.
    """
    if human_detected:
        return "STOP"
    if battery < 20:
        return "CHARGE"
    if front_obstacle:
        return "TURN"
    return "FORWARD"


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    # --- motors ---
    left = robot.getDevice("left wheel motor")
    right = robot.getDevice("right wheel motor")
    left.setPosition(float("inf"))
    right.setPosition(float("inf"))
    left.setVelocity(0.0)
    right.setVelocity(0.0)

    # --- the 8 proximity sensors, ps0..ps7 ---
    sensors = []
    for i in range(8):
        s = robot.getDevice(f"ps{i}")
        s.enable(timestep)
        sensors.append(s)

    battery = 100.0
    last_action = None

    while robot.step(timestep) != -1:
        # 1. SENSE -------------------------------------------------------
        values = [s.getValue() for s in sensors]
        # ps0 = front-right, ps7 = front-left -> the front of the robot
        front = max(values[0], values[7])
        front_obstacle = front > OBSTACLE_LEVEL
        battery -= BATTERY_DRAIN

        # 2. THINK -------------------------------------------------------
        action = decide(front_obstacle, battery)

        # Print only when the decision changes, so the console stays readable.
        if action != last_action:
            print(f"[battery {battery:5.1f}%] {action}")
            last_action = action

        # 3. ACT ---------------------------------------------------------
        if action == "FORWARD":
            left_speed, right_speed = 0.5, 0.5
        elif action == "TURN":                 # obstacle ahead -> spin right
            left_speed, right_speed = 0.5, -0.5
        else:                                  # CHARGE or STOP -> hold still
            left_speed, right_speed = 0.0, 0.0

        left.setVelocity(left_speed * MAX_SPEED)
        right.setVelocity(right_speed * MAX_SPEED)


if __name__ == "__main__":
    main()
