"""
AI Robotics Bootcamp - Lesson 11
Object-Oriented Programming for Robotics

Part 1: a simple Robot class - properties (data) and methods (actions).
Part 2: composition - a robot BUILT FROM smaller parts (Battery, Lidar,
        Motor, Brain), the way real robot software is organised.

Run with:
    python3 robot_oop.py
"""


# ---------------------------------------------------------------------------
# Part 1 - One simple class
# ---------------------------------------------------------------------------

class Robot:
    """A blueprint for a robot. Every robot built from it has its own data."""

    def __init__(self, name, battery=100):
        # __init__ runs automatically when a robot is created.
        # 'self' means THIS robot, so each robot keeps its own values.
        self.name = name
        self.battery = battery

    def greet(self):
        print(f"Hello, I am {self.name}")

    def move(self):
        if self.battery <= 0:
            print(f"{self.name} cannot move - battery empty")
            return
        self.battery -= 10          # moving costs energy
        print(f"{self.name} is moving   (battery {self.battery}%)")

    def charge(self):
        self.battery = 100          # a method can change the robot's own data
        print(f"{self.name} battery full")


def part_one():
    print("=== Part 1: one class, two robots ===")

    atlas = Robot("Atlas", 100)
    optimus = Robot("Optimus", 25)

    atlas.greet()
    optimus.greet()

    # Each object keeps its OWN battery - moving Atlas does not touch Optimus.
    atlas.move()
    optimus.move()
    print(f"Atlas: {atlas.battery}%   Optimus: {optimus.battery}%")

    optimus.charge()
    print(f"Optimus after charging: {optimus.battery}%")
    print()


# ---------------------------------------------------------------------------
# Part 2 - Composition: a robot made of parts
# ---------------------------------------------------------------------------

class Battery:
    """Stores charge and reports whether it is running low."""

    def __init__(self, level=100):
        self.level = level

    def use(self, amount):
        self.level = max(0, self.level - amount)

    def is_low(self):
        return self.level < 20


class Lidar:
    """A distance sensor. Here it just replays fake readings for the demo."""

    def __init__(self, readings):
        self.readings = readings
        self.index = 0

    def read(self):
        value = self.readings[self.index % len(self.readings)]
        self.index += 1
        return value


class Motor:
    """Turns a decision into movement."""

    def drive(self, action):
        print(f"    motors -> {action}")


class RobotBrain:
    """Decides what to do. Same priority rules as Lesson 10."""

    def decide(self, distance, battery_low):
        if battery_low:
            return "GO CHARGE"
        if distance < 0.5:
            return "TURN"
        return "FORWARD"


class SmartRobot:
    """A robot BUILT FROM parts - this is called composition.

    The robot HAS A battery, HAS A lidar, HAS A brain. Real robot software
    (and ROS 2) is organised exactly this way.
    """

    def __init__(self, name, lidar_readings):
        self.name = name
        self.battery = Battery(100)
        self.lidar = Lidar(lidar_readings)
        self.motor = Motor()
        self.brain = RobotBrain()

    def step(self):
        """One turn of the Sense -> Think -> Act loop."""
        distance = self.lidar.read()                      # SENSE
        action = self.brain.decide(distance,              # THINK
                                   self.battery.is_low())
        print(f"  sees {distance:.2f} m -> decides {action}")
        self.motor.drive(action)                          # ACT
        self.battery.use(8)


def part_two():
    print("=== Part 2: a robot built from parts ===")

    robot = SmartRobot("NaeemBot", [2.0, 1.2, 0.4, 0.3, 1.8, 2.5])

    for turn in range(1, 7):
        print(f"Step {turn}  (battery {robot.battery.level}%)")
        robot.step()
    print()


if __name__ == "__main__":
    part_one()
    part_two()
