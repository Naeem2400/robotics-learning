"""
AI Robotics Bootcamp - Lesson 42
A multi-object tracker written from scratch, in pure Python.

Production robots use ByteTrack (via YOLO). But the core idea is small enough
to build by hand, and doing so makes "track lifecycle" concrete:

  1. Match each new detection to the nearest existing track (greedy).
  2. Detections that match nothing become NEW tracks with a fresh ID.
  3. Tracks that go unmatched are kept alive for a few frames (in case the
     object was briefly hidden), then removed.

This has no dependencies, so it is unit-tested in CI. It is a simplified
version of what ByteTrack does with a Kalman filter and the Hungarian
algorithm - which are the homework for this lesson.
"""

import math
from itertools import count


class SimpleTracker:
    def __init__(self, distance_threshold=80.0, max_age=5):
        # A detection farther than this from every track starts a new track.
        self.distance_threshold = distance_threshold
        # How many frames a track survives without a matching detection.
        self.max_age = max_age
        self._ids = count(1)               # 1, 2, 3, ... never reused
        self.tracks = {}                   # id -> {"pos": (x, y), "age": int}

    def update(self, detections):
        """Advance one frame.

        detections: list of (x, y) object centres in this frame.
        returns:    list of (track_id, x, y) for the tracks seen this frame.
        """
        unmatched = list(range(len(detections)))
        assigned = {}

        # --- 1. match existing tracks to the nearest free detection ---
        for tid, track in self.tracks.items():
            best_j, best_d = None, self.distance_threshold
            for j in unmatched:
                d = _dist(track["pos"], detections[j])
                if d < best_d:
                    best_j, best_d = j, d
            if best_j is not None:
                assigned[tid] = detections[best_j]
                unmatched.remove(best_j)

        # --- 2. update matched tracks; age unmatched ones ---
        alive = {}
        for tid, track in self.tracks.items():
            if tid in assigned:
                alive[tid] = {"pos": assigned[tid], "age": 0}
            elif track["age"] + 1 <= self.max_age:
                # Keep the track alive at its last position for a few frames.
                alive[tid] = {"pos": track["pos"], "age": track["age"] + 1}
            # else: too old, drop it (this is the end of its lifecycle)

        # --- 3. every remaining detection becomes a new track ---
        for j in unmatched:
            alive[next(self._ids)] = {"pos": detections[j], "age": 0}

        self.tracks = alive

        # Report only tracks actually seen this frame (age 0).
        return [(tid, t["pos"][0], t["pos"][1])
                for tid, t in self.tracks.items() if t["age"] == 0]

    def active_ids(self):
        return sorted(self.tracks.keys())


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
