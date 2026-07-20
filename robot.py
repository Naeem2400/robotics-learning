"""
Python for Robotics - Lesson 1: Variables and Decisions

A robot program follows one cycle:
    Sensor -> Decision -> Motor -> Movement

Run with:
    python3 robot.py
"""


def project_1_robot_identity():
    """Store and print the robot's basic state."""
    print("--- Project 1: Robot identity ---")

    robot_name = "NaeemBot"
    battery = 100          # percent
    speed = 1.2            # metres per second

    print(robot_name)
    print(battery)
    print(speed)
    print()


def project_2_battery_drain():
    """A variable can be updated from its own previous value."""
    print("--- Project 2: Battery drain ---")

    battery = 80
    battery = battery - 10     # the robot used 10% of its charge
    print(battery)
    print()


def project_3_obstacle_check():
    """The sensor reading decides what the motors do."""
    print("--- Project 3: Obstacle check ---")

    distance = 15              # centimetres, from the ultrasonic sensor

    if distance < 20:
        print("Robot stop")
    else:
        print("Move")
    print()


def data_types_demo():
    """The four data types a robot uses most."""
    print("--- Data types ---")

    wheels = 4                 # int   - countable things
    distance = 1.25            # float - precise measurement, in metres
    obstacle = True            # bool  - a yes/no question
    robot_name = "Optimus"     # str   - text the robot can speak

    print("wheels    :", wheels, type(wheels).__name__)
    print("distance  :", distance, type(distance).__name__)
    print("obstacle  :", obstacle, type(obstacle).__name__)
    print("robot_name:", robot_name, type(robot_name).__name__)

    # 'if obstacle:' already means 'if obstacle is True'
    if obstacle:
        print("Stop robot")
    print()


def robot_state():
    """All of these variables together describe the robot state."""
    print("--- Robot state ---")

    battery = 95               # percent
    temperature = 30           # degrees Celsius
    speed = 1.5                # metres per second
    robot_name = "NaeemBot"
    obstacle = False

    print(f"{robot_name}: battery={battery}%, temp={temperature}C, "
          f"speed={speed} m/s, obstacle={obstacle}")
    print()


if __name__ == "__main__":
    project_1_robot_identity()
    project_2_battery_drain()
    project_3_obstacle_check()
    data_types_demo()
    robot_state()
