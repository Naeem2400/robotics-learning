"""
AI Robotics Bootcamp - Lesson 12
Sensor Explorer: see what a robot actually senses.

Reading about sensors is abstract. This controller makes it concrete:

  1. It lists EVERY device the robot has (its real hardware list).
  2. It turns slowly in place and prints live distance readings in four
     directions, as numbers and as a bar chart.

That stream of numbers is everything the robot knows about the world.

Run it from inside Webots: open worlds/sensor_lab.wbt and press Run.
"""

from controller import Robot

TURN_SPEED = 0.6          # gentle rotation so readings change slowly
PRINT_EVERY = 0.7         # seconds between printed reports
BAR_WIDTH = 20            # characters in the bar chart
BAR_MAX = 3.5             # metres represented by a full bar (lidar max range)


def list_devices(robot):
    """Print every sensor and motor this robot carries."""
    print("=" * 52)
    print("  This robot's hardware")
    print("=" * 52)

    for i in range(robot.getNumberOfDevices()):
        device = robot.getDeviceByIndex(i)
        kind = type(device).__name__          # Lidar, Motor, Camera, ...
        print(f"  {device.getName():<28} {kind}")

    print("=" * 52)
    print()


def safe_min(beams):
    """Smallest valid distance in a slice of beams (ignore 0 and infinity)."""
    valid = [d for d in beams if d > 0.0 and d != float("inf")]
    return min(valid) if valid else float("inf")


def bar(distance):
    """Draw a simple bar chart: closer object = shorter bar."""
    if distance == float("inf"):
        return "|" + " " * BAR_WIDTH + "| no echo"
    filled = int(min(distance / BAR_MAX, 1.0) * BAR_WIDTH)
    return "|" + "#" * filled + " " * (BAR_WIDTH - filled) + f"| {distance:.2f} m"


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    list_devices(robot)

    left = robot.getDevice("left wheel motor")
    right = robot.getDevice("right wheel motor")
    for motor in (left, right):
        motor.setPosition(float("inf"))
        motor.setVelocity(0.0)

    lidar = robot.getDevice("LDS-01")
    lidar.enable(timestep)

    print("Turning slowly. Watch the distances change as the robot rotates.\n")

    next_report = 0.0

    while robot.step(timestep) != -1:
        # Rotate gently in place so the view keeps changing.
        left.setVelocity(TURN_SPEED)
        right.setVelocity(-TURN_SPEED)

        now = robot.getTime()
        if now < next_report:
            continue
        next_report = now + PRINT_EVERY

        # The LDS-01 returns 360 beams (one per degree). The middle of the
        # list points straight ahead, so we can slice out four directions.
        ranges = lidar.getRangeImage()
        n = len(ranges)
        c = n // 2
        q = n // 8                       # quarter-ish sector width

        front = safe_min(ranges[c - q:c + q])
        left_d = safe_min(ranges[c + q:c + 3 * q])
        right_d = safe_min(ranges[c - 3 * q:c - q])
        back = min(safe_min(ranges[:q]), safe_min(ranges[n - q:]))

        print(f"t = {now:5.1f}s")
        print(f"  FRONT {bar(front)}")
        print(f"  LEFT  {bar(left_d)}")
        print(f"  RIGHT {bar(right_d)}")
        print(f"  BACK  {bar(back)}")
        print()


if __name__ == "__main__":
    main()
