"""
AI Robotics Bootcamp - Lesson 43
Depth estimation: turning a flat image into distance.

A normal camera gives colour but no distance. This script shows the classic,
sensor-free way a robot recovers depth: STEREO VISION - two cameras, like two
eyes. An object nearby shifts more between the two views than a far one; that
shift (the "disparity") converts directly to distance.

This needs no AI model and no download beyond a sample stereo pair. The AI
approach (Depth Anything V2) is noted at the bottom - it is a large download.

Live depth from a SINGLE camera needs a different method: stereo compares two
cameras, but one camera cannot. So --live uses a monocular AI model (MiDaS)
that estimates depth from one frame. It gives RELATIVE depth (near vs far),
not calibrated metres - great to see and to film, but a stereo/RGB-D sensor
is what you trust for a real grasp.

Usage:
    python depth_estimation.py --test              stereo on a sample pair
    python depth_estimation.py --pair L.jpg R.jpg  your own rectified pair
    python depth_estimation.py --live              live AI depth (built-in cam)
    python depth_estimation.py --live --url http://IP:8080/video   phone camera
"""

import sys
import urllib.request

# Imported so that disparity_to_depth() - pure maths - can be imported and
# unit-tested even where OpenCV cannot load (e.g. a headless CI box). The
# cv2-using entry points check for it and exit cleanly if it is missing.
try:
    import cv2
    import numpy as np
except Exception:
    cv2 = None
    np = None


def _require_cv2():
    if cv2 is None:
        print("OpenCV/NumPy not available.  pip install 'opencv-python<5'")
        sys.exit(1)

# A rectified stereo pair shipped with OpenCV (the "aloe" plant).
SAMPLE_L = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/aloeL.jpg"
SAMPLE_R = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/aloeR.jpg"


def disparity_to_depth(disparity_px, focal_px, baseline_m):
    """Convert a pixel disparity to a real distance, in metres.

        depth = (focal_length * baseline) / disparity

    The relationship is INVERSE: a large disparity (object shifted a lot
    between the two cameras) means the object is CLOSE. A tiny disparity means
    it is far away. Disparity of 0 means infinitely far, so we guard it.
    """
    if disparity_px <= 0:
        return float("inf")
    return (focal_px * baseline_m) / disparity_px


def compute_disparity(left_bgr, right_bgr):
    """Return a per-pixel disparity map from a rectified stereo pair."""
    gl = cv2.cvtColor(left_bgr, cv2.COLOR_BGR2GRAY)
    gr = cv2.cvtColor(right_bgr, cv2.COLOR_BGR2GRAY)

    block = 5
    matcher = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=112,          # must be a multiple of 16
        blockSize=block,
        P1=8 * 3 * block ** 2,       # smoothness penalties
        P2=32 * 3 * block ** 2,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32,
    )
    # SGBM returns disparity scaled by 16.
    return matcher.compute(gl, gr).astype(np.float32) / 16.0


def colour_depth(disparity):
    """Turn a disparity map into a readable colour image: near = warm."""
    valid = disparity[disparity > 0]
    lo, hi = (valid.min(), valid.max()) if valid.size else (0, 1)
    norm = np.clip((disparity - lo) / max(hi - lo, 1e-6), 0, 1)
    return cv2.applyColorMap((norm * 255).astype(np.uint8), cv2.COLORMAP_TURBO)


def fetch_sample():
    print("Fetching a sample stereo pair (one-time, ~600 KB) ...")
    urllib.request.urlretrieve(SAMPLE_L, "/tmp/aloeL.jpg")
    urllib.request.urlretrieve(SAMPLE_R, "/tmp/aloeR.jpg")
    return cv2.imread("/tmp/aloeL.jpg"), cv2.imread("/tmp/aloeR.jpg")


def run(left, right):
    disp = compute_disparity(left, right)
    valid = disp[disp > 0]

    print(f"\n  disparity: {valid.min():.1f} .. {valid.max():.1f} px "
          "(bigger = closer)")

    # Split the image into near/far halves by disparity to prove the concept.
    median = np.median(valid)
    near = (disp > median).sum()
    far = ((disp > 0) & (disp <= median)).sum()
    print(f"  pixels nearer than the median: {near:,}")
    print(f"  pixels farther than the median: {far:,}")

    # Convert a couple of disparities to real distance, with plausible optics.
    focal_px, baseline_m = 700.0, 0.06      # ~700px focal, 6 cm between cameras
    for name, d in [("nearest", valid.max()), ("median", median),
                    ("far", valid.min())]:
        depth = disparity_to_depth(d, focal_px, baseline_m)
        print(f"    {name:<8} disparity {d:6.1f} px -> ~{depth:5.2f} m away")

    out = np.hstack([left, colour_depth(disp)])
    cv2.imwrite("output_depth.jpg", out)
    print("\n  saved output_depth.jpg  (left: photo, right: depth - warm = near)")


def self_test():
    print("=" * 60)
    print("  Depth estimation (stereo) self-test")
    print("=" * 60)

    left, right = fetch_sample()
    if left is None or right is None:
        print("  Could not fetch the sample pair (no internet?).")
        return 1

    print(f"  stereo pair: {left.shape[1]} x {left.shape[0]}")
    run(left, right)

    print("\n  The depth came purely from the SHIFT between two views - no")
    print("  distance sensor, no AI model. Two eyes, like a human.")
    return 0


def run_pair(lpath, rpath):
    left, right = cv2.imread(lpath), cv2.imread(rpath)
    if left is None or right is None:
        print("Could not read one of the images.")
        return 1
    if left.shape != right.shape:
        print("The two images must be the same size (a rectified pair).")
        return 1
    run(left, right)
    return 0


def open_camera(source=None, width=640, height=480):
    if source is not None:
        cam = cv2.VideoCapture(source)
        if cam.isOpened():
            ok, frame = cam.read()
            if ok and frame is not None:
                where = source if isinstance(source, str) else f"index {source}"
                print(f"Camera ({where}): {frame.shape[1]}x{frame.shape[0]}")
                return cam
            cam.release()
        print(f"Could not open camera source: {source}")
        return None
    for index in (0, 1, 2):
        cam = cv2.VideoCapture(index)
        if cam.isOpened():
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            ok, frame = cam.read()
            if ok and frame is not None:
                print(f"Camera {index}: {frame.shape[1]}x{frame.shape[0]}")
                return cam
            cam.release()
        if index == 0:
            break
    print("\nNo camera frames. macOS grants camera permission PER APP - run this")
    print("from the terminal inside VS Code, or use a phone camera with --url.")
    return None


def live_monocular(source=None):
    """Live depth from ONE camera, using the MiDaS monocular model."""
    import time
    try:
        import torch
    except ImportError:
        print("PyTorch missing.  pip install torch timm")
        return 1

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Loading MiDaS depth model on {device} (first run downloads it) ...")

    # MiDaS pulls its backbone from a NESTED repo whose load does not carry
    # trust_repo=True, so torch.hub stops to ask an interactive "do you trust
    # this repo?" question - which hangs with no terminal. We are deliberately
    # loading MiDaS, so disable that check for this process.
    import torch.hub
    torch.hub._check_repo_is_trusted = lambda *a, **k: None

    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small", trust_repo=True)
    midas.to(device).eval()
    transform = torch.hub.load("intel-isl/MiDaS", "transforms",
                               trust_repo=True).small_transform

    cam = open_camera(source)
    if cam is None:
        return 1

    print("  Warm = near, cool = far. Press Q to quit.\n")
    frames, started, misses = 0, time.time(), 0

    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        inp = transform(rgb).to(device)
        with torch.no_grad():
            pred = midas(inp)
            pred = torch.nn.functional.interpolate(
                pred.unsqueeze(1), size=frame.shape[:2],
                mode="bicubic", align_corners=False).squeeze()
        depth = pred.cpu().numpy()

        depth_colour = colour_depth(depth - depth.min() + 1e-3)
        view = np.hstack([frame, depth_colour])

        frames += 1
        fps = frames / max(time.time() - started, 1e-6)
        cv2.putText(view, f"{fps:.1f} fps  (relative depth)", (12, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Monocular Depth (left: camera, right: depth)", view)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"\n  Ran at about {fps:.1f} fps.")
    return 0


def main():
    _require_cv2()

    if "--live" in sys.argv:
        source = None
        if "--cam" in sys.argv:
            source = int(sys.argv[sys.argv.index("--cam") + 1])
        elif "--url" in sys.argv:
            source = sys.argv[sys.argv.index("--url") + 1]
        sys.exit(live_monocular(source))

    if "--pair" in sys.argv:
        i = sys.argv.index("--pair")
        if i + 2 >= len(sys.argv):
            print("Usage: python depth_estimation.py --pair left.jpg right.jpg")
            sys.exit(1)
        sys.exit(run_pair(sys.argv[i + 1], sys.argv[i + 2]))

    # Default and --test both run the sample stereo demo.
    sys.exit(self_test())


if __name__ == "__main__":
    main()
