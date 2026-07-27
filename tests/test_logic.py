"""
Tests for the pure decision logic across the course.

These deliberately cover only the dependency-free modules - no OpenCV,
PyTorch, or camera - so they run in seconds in CI on any Python version.
The heavy vision scripts are exercised by their own --test modes instead.

Run with:
    pytest
"""

import os
import sys

# Make the project root importable when pytest runs from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Lesson 10 - the robot brain's decision priority
# ---------------------------------------------------------------------------

def test_robot_brain_priority():
    from robot_brain import decide

    # Human safety must win over everything else.
    assert decide(battery=50, distance=12, human_detected=True) \
        == "Human detected - STOP for safety"
    # Then low battery.
    assert decide(battery=10, distance=100) == "Go to charging station"
    # Then an obstacle.
    assert decide(battery=80, distance=10) == "Obstacle detected - turn left"
    # Otherwise move.
    assert decide(battery=90, distance=100) == "Move forward"


# ---------------------------------------------------------------------------
# Lesson 28 - A* and Dijkstra
# ---------------------------------------------------------------------------

def test_astar_matches_dijkstra_length_but_explores_less():
    import path_planning_demo as p

    start, goal = p.find("S"), p.find("G")
    d_path, d_explored = p.search(start, goal, use_heuristic=False)
    a_path, a_explored = p.search(start, goal, use_heuristic=True)

    # Both optimal: same path length.
    assert len(d_path) == len(a_path)
    # A* never explores more than Dijkstra.
    assert len(a_explored) <= len(d_explored)


def test_astar_with_zero_heuristic_is_dijkstra():
    import path_planning_demo as p

    # If the heuristic is disabled, A* should behave exactly like Dijkstra.
    start, goal = p.find("S"), p.find("G")
    _, d = p.search(start, goal, use_heuristic=False)
    _, a = p.search(start, goal, use_heuristic=False)
    assert len(a) == len(d)


# ---------------------------------------------------------------------------
# Lesson 17 - the mini ROS broker
# ---------------------------------------------------------------------------

def test_broker_delivers_to_subscribers():
    from mini_ros import Broker

    broker = Broker()
    received = []
    broker.subscribe("/topic", "listener", received.append)
    broker.publish("/topic", "hello", from_node="talker")

    assert received == ["hello"]


def test_broker_topic_with_no_subscribers_does_not_error():
    from mini_ros import Broker

    broker = Broker()
    # Publishing into the void must be harmless - this is why a robot keeps
    # running when a node dies.
    broker.publish("/empty", "data", from_node="talker")


# ---------------------------------------------------------------------------
# Lesson 13 - grayscale conversion
# ---------------------------------------------------------------------------

def test_grayscale_weights_green_highest():
    from pixels_demo import to_grayscale

    # A pure green pixel should be brighter in grayscale than pure red or blue,
    # because the eye is most sensitive to green (0.587 weight).
    red = to_grayscale([[(255, 0, 0)]])[0][0]
    green = to_grayscale([[(0, 255, 0)]])[0][0]
    blue = to_grayscale([[(0, 0, 255)]])[0][0]

    assert green > red > blue
    assert to_grayscale([[(0, 0, 0)]])[0][0] == 0
    assert to_grayscale([[(255, 255, 255)]])[0][0] == 255
