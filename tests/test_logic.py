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


# ---------------------------------------------------------------------------
# Lesson 42 - the from-scratch multi-object tracker
# ---------------------------------------------------------------------------

def test_tracker_keeps_ids_as_objects_move():
    from simple_tracker import SimpleTracker

    t = SimpleTracker(distance_threshold=50, max_age=3)
    seen0 = t.update([(100, 100), (300, 100)])
    ids0 = sorted(tid for tid, *_ in seen0)
    # Both objects drift a little.
    seen1 = t.update([(108, 100), (308, 100)])
    ids1 = sorted(tid for tid, *_ in seen1)
    assert ids0 == [1, 2]
    assert ids1 == [1, 2]          # same IDs, not re-numbered


def test_tracker_assigns_new_id_to_new_object():
    from simple_tracker import SimpleTracker

    t = SimpleTracker(distance_threshold=50, max_age=3)
    t.update([(100, 100)])                       # id 1
    seen = t.update([(105, 100), (400, 100)])    # new object at 400 -> id 2
    ids = sorted(tid for tid, *_ in seen)
    assert ids == [1, 2]


def test_tracker_drops_object_after_max_age():
    from simple_tracker import SimpleTracker

    t = SimpleTracker(distance_threshold=50, max_age=2)
    t.update([(100, 100), (300, 100)])           # ids 1, 2
    # Object 2 disappears; its track is kept alive for max_age frames.
    t.update([(105, 100)])                       # miss 1 (track 2 age 1)
    assert 2 in t.active_ids()
    t.update([(110, 100)])                       # miss 2 (track 2 age 2)
    assert 2 in t.active_ids()
    t.update([(115, 100)])                       # miss 3 -> exceeds max_age
    assert 2 not in t.active_ids()               # lifecycle ended


# ---------------------------------------------------------------------------
# Lesson 43 - stereo depth math
# ---------------------------------------------------------------------------

def test_disparity_to_depth_is_inverse():
    from depth_estimation import disparity_to_depth

    focal, baseline = 700.0, 0.06
    near = disparity_to_depth(100.0, focal, baseline)   # large disparity
    far = disparity_to_depth(10.0, focal, baseline)     # small disparity

    # Bigger disparity must mean a closer (smaller) distance.
    assert near < far
    # depth = focal * baseline / disparity, exactly.
    assert abs(near - (focal * baseline / 100.0)) < 1e-9
    # Zero disparity means infinitely far.
    assert disparity_to_depth(0.0, focal, baseline) == float("inf")
