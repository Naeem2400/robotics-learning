"""
AI Robotics Bootcamp - Lesson 44
Visual SLAM: a robot builds a map of an unknown place, and finds itself in it.

Nobody hands the robot a floor plan. It watches a moving camera, tracks
features, estimates its own motion (odometry), and draws a trajectory - the
same sense-decide-act loop as every earlier lesson, now for "where am I?"

This is visual odometry, the front-end of visual SLAM. A production system
(ORB-SLAM3, RTAB-Map, Cartographer) adds loop closure, a bundle-adjusted map,
and often an IMU. The demo shows those ideas on a real HD clip so the output
is something you can post.

The default clip is a Mixkit library walkthrough - Full HD, free commercial
licence, no faces, lots of unique corners for the tracker. First run
downloads it into video_out/ (gitignored). Pass --video to use your own.

Usage:
    python visual_slam.py --test
    python visual_slam.py --linkedin
    python visual_slam.py --video path.mp4 --linkedin
    python visual_slam.py --linkedin --reel
    python visual_slam.py --linkedin --gif
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import urllib.request
from collections import deque
from pathlib import Path

try:
    import cv2
    import numpy as np
except Exception:
    cv2 = None
    np = None


ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "video_out"
ASSETS_DIR = ROOT / "assets"

# Mixkit #21589 - "Walking down a library corridor with tables and bookcases"
# 1920x1080, 24 fps, ~17 s. Mixkit Stock Video Free License: commercial use
# allowed, attribution not required (we credit it anyway).
STOCK_URL = "https://assets.mixkit.co/videos/21589/21589-1080.mp4"
STOCK_PATH = VIDEO_DIR / "stock_library_corridor_1080.mp4"
STOCK_CREDIT = "Mixkit #21589  ·  free commercial licence"

NAVY = (22, 16, 8)
CYAN = (255, 220, 40)
AMBER = (0, 176, 255)
MAGENTA = (160, 80, 255)
WHITE = (245, 245, 245)
MUTED = (170, 175, 185)
GREEN = (80, 220, 140)


def _require_cv2():
    if cv2 is None:
        print("OpenCV/NumPy not available.  source .venv/bin/activate")
        sys.exit(1)


def wrap_angle(theta):
    """Keep an angle in (-pi, pi]. Pure maths - safe to unit-test."""
    return (theta + math.pi) % (2 * math.pi) - math.pi


def compose_pose(x, y, theta, forward, yaw):
    """Integrate a robot-frame step into world coordinates.

    `forward` is distance travelled along the robot's current heading,
    `yaw` is the change in heading. This is the odometry update a wheeled
    robot (or a camera walking down a corridor) performs every frame.
    """
    new_theta = wrap_angle(theta + yaw)
    return x + forward * math.cos(new_theta), y + forward * math.sin(new_theta), new_theta


def loop_closure_triggered(distance_from_start, match_ratio, min_distance=8.0, min_ratio=0.28):
    """A loop closes when we are far from home AND we recognise the start."""
    return distance_from_start >= min_distance and match_ratio >= min_ratio


def download_stock_video(dest=STOCK_PATH, url=STOCK_URL):
    """Fetch the Mixkit clip if it is not already on disk."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1_000_000:
        print(f"  stock clip already on disk: {dest.name}")
        return dest
    print(f"  downloading free HD clip (~55 MB) ...")
    print(f"  {url}")

    def _progress(block, block_size, total):
        if total <= 0:
            return
        done = min(100, int(100 * block * block_size / total))
        bar = "#" * (done // 2) + "-" * (50 - done // 2)
        sys.stdout.write(f"\r  [{bar}] {done:3d}%")
        sys.stdout.flush()

    urllib.request.urlretrieve(url, dest, _progress)
    sys.stdout.write("\n")
    return dest


def camera_matrix(width, height):
    """A plausible pinhole model when the stock clip is uncalibrated."""
    focal = 0.90 * width
    return np.array(
        [[focal, 0, width / 2.0],
         [0, focal, height / 2.0],
         [0, 0, 1.0]],
        dtype=np.float64,
    )


def _put(img, text, org, scale=0.55, color=WHITE, thickness=1):
    cv2.putText(
        img, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA
    )


def title_card(size, seconds=2.5, fps=24):
    """Opening frames: the hook, readable with the sound off."""
    w, h = size
    frames = []
    n = max(1, int(seconds * fps))
    for i in range(n):
        canvas = np.full((h, w, 3), NAVY, dtype=np.uint8)
        fade = min(1.0, i / max(n * 0.25, 1))
        col = tuple(int(c * fade) for c in WHITE)
        _put(canvas, "HOW DOES A ROBOT BUILD A MAP", (90, h // 2 - 40), 1.15, col, 2)
        _put(canvas, "WHEN NOBODY GIVES IT ONE?", (90, h // 2 + 20), 1.15, col, 2)
        accent = tuple(int(c * fade) for c in CYAN)
        _put(canvas, "Lesson 44   ·   Visual SLAM   ·   mapping + localization at once",
             (90, h // 2 + 90), 0.7, accent, 1)
        frames.append(canvas)
    return frames


def end_card(size, seconds=3.0, fps=24):
    w, h = size
    frames = []
    n = max(1, int(seconds * fps))
    for _ in range(n):
        canvas = np.full((h, w, 3), NAVY, dtype=np.uint8)
        _put(canvas, "THE ROBOT IS SIMULTANEOUSLY", (90, h // 2 - 50), 1.05, WHITE, 2)
        _put(canvas, "LEARNING THE WORLD", (90, h // 2 + 10), 1.05, CYAN, 2)
        _put(canvas, "AND FINDING ITSELF INSIDE IT.", (90, h // 2 + 70), 1.05, WHITE, 2)
        _put(canvas, "Mapping  +  Localization  =  SLAM", (90, h - 80), 0.7, AMBER, 1)
        frames.append(canvas)
    return frames


def seed_features(gray):
    return cv2.goodFeaturesToTrack(
        gray,
        maxCorners=500,
        qualityLevel=0.01,
        minDistance=8,
        blockSize=7,
    )


def estimate_step(prev_pts, curr_pts, width):
    """Turn tracked point motion into a (forward, yaw) odometry step.

    A corridor walk is mostly forward translation. Mean horizontal flow is
    yaw; expansion away from the image centre is forward speed. This is
    cheaper and more stable on uncalibrated stock footage than recoverPose,
    which needs a true calibrated camera.
    """
    flow = curr_pts - prev_pts
    yaw = -float(np.median(flow[:, 0])) * (0.85 / width)

    cx = width / 2.0
    radial_prev = np.abs(prev_pts[:, 0] - cx)
    radial_curr = np.abs(curr_pts[:, 0] - cx)
    # Points sliding away from the centre mean the camera is moving forward.
    expansion = float(np.median(radial_curr - radial_prev))
    speed = float(np.median(np.linalg.norm(flow, axis=1)))
    forward = max(0.0, expansion) * 0.045 + speed * 0.012
    # Ignore tiny jitter so the map does not vibrate on a still frame.
    if forward < 0.04 and abs(yaw) < 0.003:
        return 0.0, 0.0
    return forward, yaw


def match_ratio_orb(orb, desc_a, gray_b):
    """How similar is this frame to the start? Used for loop-closure."""
    if desc_a is None:
        return 0.0
    kps, desc_b = orb.detectAndCompute(gray_b, None)
    if desc_b is None or len(kps) < 20:
        return 0.0
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    knn = matcher.knnMatch(desc_a, desc_b, k=2)
    good = 0
    total = 0
    for pair in knn:
        if len(pair) < 2:
            continue
        best, second = pair
        total += 1
        if best.distance < 0.75 * second.distance:
            good += 1
    return good / total if total else 0.0


def draw_tracks(frame, tracks):
    """Paint fading feature trails - this is what the robot is 'seeing'."""
    overlay = frame.copy()
    for trail in tracks:
        if len(trail) < 2:
            continue
        pts = np.array(trail, dtype=np.int32)
        cv2.polylines(overlay, [pts], False, CYAN, 1, cv2.LINE_AA)
        x, y = trail[-1]
        cv2.circle(overlay, (int(x), int(y)), 3, AMBER, -1, cv2.LINE_AA)
    return cv2.addWeighted(overlay, 0.85, frame, 0.15, 0)


def landmarks_from_features(x, y, theta, pts, width, depth_scale=5.5):
    """Sketch walls beside the robot from where features sit in the image.

    A point on the left of the frame becomes a landmark to the robot's left.
    This is not metric mapping — it is the visual-SLAM intuition: the camera
    is carving a corridor of observed points as it moves.
    """
    marks = []
    cx = width / 2.0
    for px, py in pts:
        offset = (px - cx) / max(cx, 1.0)
        side = offset * depth_scale
        marks.append((x - math.sin(theta) * side, y + math.cos(theta) * side))
    return marks


def draw_map(size, poses, landmarks, looped, match_ratio):
    """Bird's-eye view of the estimated trajectory and sketched landmarks."""
    w, h = size
    canvas = np.full((h, w, 3), (28, 20, 12), dtype=np.uint8)
    for x in range(0, w, 40):
        cv2.line(canvas, (x, 0), (x, h), (40, 32, 22), 1)
    for y in range(0, h, 40):
        cv2.line(canvas, (0, y), (w, y), (40, 32, 22), 1)

    _put(canvas, "MAP", (16, 32), 0.7, CYAN, 2)
    _put(canvas, "where am I?", (16, 58), 0.45, MUTED, 1)

    if not poses:
        _put(canvas, "waiting for motion ...", (16, h // 2), 0.5, MUTED, 1)
        return canvas

    xs = [p[0] for p in poses] + [p[0] for p in landmarks]
    ys = [p[1] for p in poses] + [p[1] for p in landmarks]
    pad = 40
    span = max(max(xs) - min(xs), max(ys) - min(ys), 4.0)
    scale = min((w - 2 * pad) / span, (h - 2 * pad - 40) / span)
    min_x, min_y = min(xs), min(ys)

    def to_px(x, y):
        px = int(pad + (x - min_x) * scale)
        py = int(h - pad - (y - min_y) * scale)
        return px, py

    for lx, ly in landmarks:
        cv2.circle(canvas, to_px(lx, ly), 1, (90, 70, 40), -1, cv2.LINE_AA)

    pts = [to_px(x, y) for x, y, _ in poses]
    cv2.polylines(canvas, [np.array(pts, dtype=np.int32)], False, CYAN, 2, cv2.LINE_AA)
    sx, sy = pts[0]
    cv2.circle(canvas, (sx, sy), 7, GREEN, -1, cv2.LINE_AA)
    _put(canvas, "START", (sx + 10, sy - 8), 0.4, GREEN, 1)

    x, y, theta = poses[-1]
    px, py = pts[-1]
    tip = (int(px + 18 * math.cos(theta)), int(py - 18 * math.sin(theta)))
    left = (int(px + 10 * math.cos(theta + 2.5)), int(py - 10 * math.sin(theta + 2.5)))
    right = (int(px + 10 * math.cos(theta - 2.5)), int(py - 10 * math.sin(theta - 2.5)))
    cv2.fillConvexPoly(canvas, np.array([tip, left, right], dtype=np.int32), AMBER)

    dist = math.hypot(x - poses[0][0], y - poses[0][1])
    _put(canvas, f"path  {dist:.1f}  (relative)", (16, h - 48), 0.45, WHITE, 1)
    status = "LOOP CLOSED" if looped else f"loop search  {match_ratio * 100:.0f}%"
    color = MAGENTA if looped else MUTED
    _put(canvas, status, (16, h - 22), 0.5, color, 1)
    return canvas


def compose_dashboard(camera, mapping, pose, n_tracks, match_ratio, fps, looped, credit):
    """1920x1080 LinkedIn frame: camera + map + teaching HUD."""
    W, H = 1920, 1080
    canvas = np.full((H, W, 3), NAVY, dtype=np.uint8)

    cam = cv2.resize(camera, (1280, 720))
    mapping = cv2.resize(mapping, (560, 720))
    canvas[80:800, 40:1320] = cam
    canvas[80:800, 1340:1900] = mapping

    cv2.rectangle(canvas, (0, 0), (W, 72), (32, 24, 14), -1)
    _put(canvas, "VISUAL SLAM", (32, 46), 0.95, CYAN, 2)
    _put(canvas, "Simultaneous Localization and Mapping", (360, 46), 0.65, WHITE, 1)

    cv2.rectangle(canvas, (0, 820), (W, H), (32, 24, 14), -1)
    x, y, theta = pose
    _put(canvas, f"FEATURES  {n_tracks}", (32, 870), 0.7, AMBER, 2)
    _put(canvas, f"POSE  x {x:6.1f}   y {y:6.1f}   yaw {math.degrees(theta):6.1f} deg",
         (32, 920), 0.6, WHITE, 1)
    _put(canvas, "MAPPING: drawing the world     LOCALIZATION: estimating this pose",
         (32, 970), 0.5, MUTED, 1)
    _put(canvas, f"{fps:4.1f} fps   ·   {credit}", (32, 1045), 0.45, MUTED, 1)

    tag = "LOOP CLOSURE" if looped else "ODOMETRY  (wheel-less, from the camera)"
    color = MAGENTA if looped else CYAN
    _put(canvas, tag, (1100, 870), 0.65, color, 2)
    _put(canvas, "Nobody gave this robot a map.", (1100, 920), 0.55, WHITE, 1)
    return canvas


def to_vertical(frame):
    """9:16 reel: crop the dashboard to a phone-shaped centre slice."""
    h, w = frame.shape[:2]
    target_w = int(h * 9 / 16)
    x0 = max(0, (w - target_w) // 2)
    return frame[:, x0:x0 + target_w]


def run_visual_slam(video_path, out_path, max_seconds=None, make_reel=False, make_gif=False):
    _require_cv2()
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Could not open {video_path}")
        sys.exit(1)

    src_fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    print(f"  source: {src_w}x{src_h}  {src_fps:.1f} fps  {total} frames")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = Path(out_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, src_fps, (1920, 1080))

    reel_writer = None
    reel_path = out_path.with_name(out_path.stem + "_vertical.mp4")
    if make_reel:
        reel_writer = cv2.VideoWriter(str(reel_path), fourcc, src_fps, (608, 1080))

    for card in title_card((1920, 1080), fps=src_fps):
        writer.write(card)
        if reel_writer is not None:
            reel_writer.write(cv2.resize(to_vertical(card), (608, 1080)))

    ok, frame = cap.read()
    if not ok:
        print("Empty video.")
        sys.exit(1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_pts = seed_features(gray)
    tracks = []
    if prev_pts is not None:
        tracks = [deque([(float(x), float(y))], maxlen=12) for x, y in prev_pts.reshape(-1, 2)]

    orb = cv2.ORB_create(nfeatures=800)
    _, start_desc = orb.detectAndCompute(gray, None)

    x = y = theta = 0.0
    poses = [(0.0, 0.0, 0.0)]
    landmarks = []
    looped = False
    match_ratio = 0.0
    poster = None
    n_written = 0
    max_frames = int(max_seconds * src_fps) if max_seconds else None

    lk_params = dict(
        winSize=(21, 21),
        maxLevel=3,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
    )

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray_now = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_pts is not None and len(prev_pts) >= 8:
            nxt, status, _ = cv2.calcOpticalFlowPyrLK(gray, gray_now, prev_pts, None, **lk_params)
            good_new, good_old, kept = [], [], []
            for i, (st, trail) in enumerate(zip(status.reshape(-1), tracks)):
                if st != 1:
                    continue
                p_new = nxt[i].reshape(2)
                p_old = prev_pts[i].reshape(2)
                good_new.append(p_new)
                good_old.append(p_old)
                trail.append((float(p_new[0]), float(p_new[1])))
                kept.append(trail)
            tracks = kept
            if len(good_new) >= 8:
                curr = np.array(good_new, dtype=np.float32)
                prev = np.array(good_old, dtype=np.float32)
                forward, yaw = estimate_step(prev, curr, frame.shape[1])
                x, y, theta = compose_pose(x, y, theta, forward, yaw)
                poses.append((x, y, theta))
                if n_written % 3 == 0:
                    sample = curr[::5]
                    landmarks.extend(
                        landmarks_from_features(x, y, theta, sample, frame.shape[1])
                    )
                    if len(landmarks) > 900:
                        landmarks = landmarks[-900:]
                prev_pts = curr.reshape(-1, 1, 2)
            else:
                prev_pts = seed_features(gray_now)
                tracks = []
                if prev_pts is not None:
                    tracks = [deque([(float(px), float(py))], maxlen=12)
                              for px, py in prev_pts.reshape(-1, 2)]
        else:
            prev_pts = seed_features(gray_now)
            tracks = []
            if prev_pts is not None:
                tracks = [deque([(float(px), float(py))], maxlen=12)
                          for px, py in prev_pts.reshape(-1, 2)]

        if n_written % 8 == 0:
            match_ratio = match_ratio_orb(orb, start_desc, gray_now)
            dist = math.hypot(x, y)
            if loop_closure_triggered(dist, match_ratio):
                looped = True

        if prev_pts is None or len(tracks) < 80:
            extra = seed_features(gray_now)
            if extra is not None:
                existing = { (int(t[-1][0]) // 8, int(t[-1][1]) // 8) for t in tracks if t }
                for px, py in extra.reshape(-1, 2):
                    key = (int(px) // 8, int(py) // 8)
                    if key in existing:
                        continue
                    tracks.append(deque([(float(px), float(py))], maxlen=12))
                    existing.add(key)
                prev_pts = np.array([t[-1] for t in tracks], dtype=np.float32).reshape(-1, 1, 2)

        cam = draw_tracks(frame, tracks)
        mapping = draw_map((560, 720), poses, landmarks, looped, match_ratio)
        dash = compose_dashboard(
            cam, mapping, (x, y, theta), len(tracks), match_ratio,
            src_fps, looped, STOCK_CREDIT,
        )
        writer.write(dash)
        if reel_writer is not None:
            reel_writer.write(cv2.resize(to_vertical(dash), (608, 1080)))
        if poster is None and n_written >= 150:
            poster = dash.copy()

        gray = gray_now
        n_written += 1
        if n_written % 40 == 0:
            print(f"  frame {n_written}/{total or '?'}  tracks={len(tracks)}  pose=({x:.1f}, {y:.1f})")
        if max_frames and n_written >= max_frames:
            break

    cap.release()

    for card in end_card((1920, 1080), fps=src_fps):
        writer.write(card)
        if reel_writer is not None:
            reel_writer.write(cv2.resize(to_vertical(card), (608, 1080)))

    writer.release()
    if reel_writer is not None:
        reel_writer.release()

    def _to_h264(path):
        """LinkedIn (and most browsers) play H.264, not OpenCV's mp4v."""
        path = Path(path)
        if not path.exists():
            return
        tmp = path.with_suffix(".h264.mp4")
        cmd = (
            f'ffmpeg -y -i "{path}" -c:v libx264 -pix_fmt yuv420p -crf 18 '
            f'-preset fast -movflags +faststart "{tmp}" -loglevel error'
        )
        if os.system(cmd) == 0 and tmp.exists() and tmp.stat().st_size > 1000:
            tmp.replace(path)

    _to_h264(out_path)
    if make_reel:
        _to_h264(reel_path)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    poster_path = ASSETS_DIR / "visual-slam-poster.jpg"
    if poster is not None:
        cv2.imwrite(str(poster_path), poster)

    print()
    print(f"  LinkedIn landscape: {out_path}")
    if make_reel:
        print(f"  vertical reel:      {reel_path}")
    print(f"  poster:             {poster_path}")
    print(f"  trajectory points:  {len(poses)}")
    print(f"  loop closed:        {looped}")

    if make_gif:
        gif_path = ASSETS_DIR / "visual-slam-demo.gif"
        cmd = (
            f'ffmpeg -y -ss 3 -i "{out_path}" -vf "fps=12,scale=720:-1:flags=lanczos" '
            f'-t 8 "{gif_path}"'
        )
        print(f"  building GIF ...")
        os.system(cmd)
        if gif_path.exists():
            print(f"  GIF:                {gif_path}  ({gif_path.stat().st_size / 1e6:.1f} MB)")

    return out_path


def run_test():
    """No video, no network: prove the odometry maths and a tiny synthetic walk."""
    _require_cv2()
    x = y = theta = 0.0
    for _ in range(10):
        x, y, theta = compose_pose(x, y, theta, forward=1.0, yaw=0.0)
    assert abs(x - 10.0) < 1e-9 and abs(y) < 1e-9

    x = y = theta = 0.0
    # A quarter-circle of 90 one-degree left turns.
    for _ in range(90):
        x, y, theta = compose_pose(x, y, theta, forward=0.1, yaw=math.radians(1))
    assert abs(wrap_angle(theta - math.pi / 2)) < 0.05
    assert y > 2  # ended up off the original axis

    assert not loop_closure_triggered(1.0, 0.9)
    assert loop_closure_triggered(12.0, 0.4)
    assert not loop_closure_triggered(12.0, 0.1)

    # 12 synthetic frames of a textured wall sliding left = camera turning right.
    frames = []
    wall = np.zeros((240, 320), dtype=np.uint8)
    rng = np.random.default_rng(0)
    for _ in range(80):
        x0, y0 = rng.integers(10, 310), rng.integers(10, 230)
        cv2.circle(wall, (int(x0), int(y0)), 3, 255, -1)
    for shift in range(12):
        frames.append(np.roll(wall, -shift * 3, axis=1))

    prev = frames[0]
    pts = seed_features(prev)
    assert pts is not None and len(pts) > 10
    nxt, status, _ = cv2.calcOpticalFlowPyrLK(prev, frames[-1], pts, None)
    moved = nxt[status.reshape(-1) == 1]
    assert len(moved) > 5

    print("  Lesson 44 tests passed.")
    print("  odometry integrates, loop-closure needs BOTH distance and recognition,")
    print("  and optical flow tracks a moving texture.")
    print()
    print("  Next: python visual_slam.py --linkedin")


def parse_args():
    p = argparse.ArgumentParser(description="Lesson 44 — visual SLAM on a free HD clip")
    p.add_argument("--test", action="store_true", help="no video, just the maths")
    p.add_argument("--video", help="your own clip (otherwise the Mixkit library tour)")
    p.add_argument("--linkedin", action="store_true",
                   help="render a 1920x1080 overlay for LinkedIn")
    p.add_argument("--reel", action="store_true", help="also export a 9:16 vertical cut")
    p.add_argument("--gif", action="store_true", help="also export an 8-second README GIF")
    p.add_argument("--seconds", type=float, default=None,
                   help="process only the first N seconds of the clip")
    p.add_argument("--out", default=str(VIDEO_DIR / "slam_linkedin_landscape.mp4"))
    return p.parse_args()


def main():
    args = parse_args()
    print("=" * 62)
    print("  Lesson 44 - Visual SLAM")
    print("=" * 62)
    print()

    if args.test:
        run_test()
        return

    if not args.linkedin and args.video is None:
        # Default action is the LinkedIn render - that is the whole point.
        args.linkedin = True

    if args.video:
        source = Path(args.video)
        if not source.exists():
            print(f"  file not found: {source}")
            sys.exit(1)
    else:
        source = download_stock_video()

    run_visual_slam(
        source,
        args.out,
        max_seconds=args.seconds,
        make_reel=args.reel,
        make_gif=args.gif,
    )
    print()
    print("  Post the landscape mp4 on LinkedIn. Caption is in")
    print("  docs/reel-scripts.md  (Reel 7) and lessons/lesson-44-slam.md.")


if __name__ == "__main__":
    main()
