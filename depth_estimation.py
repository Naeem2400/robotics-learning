"""
AI Robotics Bootcamp - Lesson 43
Depth estimation: turning a flat image into distance.

A normal camera gives colour but no distance. This script shows the classic,
sensor-free way a robot recovers depth: STEREO VISION - two cameras, like two
eyes. An object nearby shifts more between the two views than a far one; that
shift (the "disparity") converts directly to distance.

This needs no AI model and no download beyond a sample stereo pair. The AI
approach (Depth Anything V2) is noted at the bottom - it is a large download.

Usage:
    python depth_estimation.py --test              stereo on a sample pair
    python depth_estimation.py --pair L.jpg R.jpg  your own rectified pair
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


def main():
    _require_cv2()
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
