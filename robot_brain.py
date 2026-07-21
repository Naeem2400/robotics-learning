"""
AI Robotics Bootcamp - Lesson 10
The robot's brain: Sense -> Think -> Act

This file has two parts:
  1. decide()  - the "Think" step: given sensor data, choose an action.
  2. A small Finite State Machine (FSM) showing how a robot moves
     through states like SEARCH -> MOVE -> PICK.

Run with:
    python3 robot_brain.py
"""


# ---------------------------------------------------------------------------
# Part 1 - The decision function (the "Think" step)
# ---------------------------------------------------------------------------

def decide(battery, distance, human_detected=False):
    """Choose one action from the current sensor readings.

    The ORDER of these checks is the robot's list of priorities. Safety is
    checked first, so a detected human always wins - even when the battery is
    fine and an obstacle is near. This is the answer to the lesson challenge.
    """
    if human_detected:
        return "Human detected - STOP for safety"
    if battery < 20:
        return "Go to charging station"
    if distance < 20:
        return "Obstacle detected - turn left"
    return "Move forward"


def test_decisions():
    """Run the decision function on a few scenarios and print the results."""
    print("=== Part 1: Decision function ===")

    # (battery, distance, human_detected)
    scenarios = [
        (10, 100, False),   # low battery -> charge
        (80,  10, False),   # obstacle    -> turn left
        (90, 100, False),   # all clear   -> move
        (50,  12, True),    # the challenge: human wins over everything
    ]

    for battery, distance, human in scenarios:
        action = decide(battery, distance, human)
        print(f"battery={battery:>3}%  distance={distance:>3}cm  "
              f"human={str(human):<5} -> {action}")
    print()


# ---------------------------------------------------------------------------
# Part 2 - A simple Finite State Machine
# ---------------------------------------------------------------------------

def run_state_machine():
    """Walk a warehouse robot through its states, one step at a time.

    The robot is always in exactly ONE state. Each state decides which state
    comes next. This is the same idea used in ROS 2 and industrial robots.
    """
    print("=== Part 2: Finite State Machine ===")

    state = "SEARCH"
    steps = 0

    while state != "DONE":
        steps += 1

        if state == "SEARCH":
            print(f"[{state}] Looking for the object...")
            state = "MOVE"          # object found

        elif state == "MOVE":
            print(f"[{state}] Moving to the object...")
            state = "PICK"

        elif state == "PICK":
            print(f"[{state}] Picking up the object...")
            state = "RETURN"

        elif state == "RETURN":
            print(f"[{state}] Returning to base...")
            state = "DONE"

        # Safety valve: never loop forever.
        if steps > 20:
            print("Too many steps - stopping.")
            break

    print(f"[{state}] Mission complete in {steps} steps.")
    print()


if __name__ == "__main__":
    test_decisions()
    run_state_machine()
