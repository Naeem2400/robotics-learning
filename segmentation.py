"""
AI Robotics Bootcamp - Lesson 41
Image segmentation: from a box to the exact object shape.

YOLO detection draws a rectangle around an object. A robot arm cannot grasp
from a rectangle - it needs the object's real outline. Segmentation gives
every pixel a label, so the arm knows exactly where the object is and where
its centre-of-mass is.

This uses YOLO's segmentation model, which needs no new install (ultralytics
is already set up). SAM2 is the state of the art but is a large download;
the concepts here transfer to it directly.

Usage:
    python segmentation.py --test           run on a sample image, no camera
    python segmentation.py --image f.jpg    segment an image file
    python segmentation.py                  live camera (built-in)
    python segmentation.py --cam 1          use camera device 1 (e.g. iPhone)
    python segmentation.py --url http://192.168.1.42:8080/video   phone stream
"""

import sys

try:
    import cv2
    import numpy as np
    from ultralytics import YOLO
except ImportError as e:
    print(f"Missing dependency: {e.name}")
    print("  pip install 'opencv-python<5' ultralytics")
    sys.exit(1)

MODEL_NAME = "yolo11n-seg.pt"      # the '-seg' model outputs masks, not just boxes
CONFIDENCE = 0.5


def grasp_point(mask):
    """The centroid of a mask - a far better place for a robot to grasp than
    the centre of a bounding box.

    The box centre can sit on background (think of an L-shaped or tilted
    object); the mask centroid is always on the object itself.
    """
    ys, xs = np.where(mask > 0.5)
    if len(xs) == 0:
        return None
    return int(xs.mean()), int(ys.mean())


def analyse(result, model):
    """Return, per object: label, box area, mask area, and grasp point."""
    out = []
    if result.masks is None:
        return out

    h, w = result.orig_shape
    for i, box in enumerate(result.boxes):
        label = model.names[int(box.cls[0])]
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        box_area = (x2 - x1) * (y2 - y1)

        mask = result.masks.data[i].cpu().numpy()
        # The mask is at model resolution; scale its pixel count to the image.
        mask_px = mask.sum() * (w * h) / (mask.shape[1] * mask.shape[0])

        # Resize the mask to image size to find the grasp point in real coords.
        full = cv2.resize(mask, (w, h))
        grasp = grasp_point(full)

        out.append({
            "label": label,
            "box_area": box_area,
            "mask_area": mask_px,
            "fill": mask_px / box_area if box_area else 0,
            "grasp": grasp,
        })
    return out


def annotate(result, analysis):
    """Draw the masks (via YOLO) plus the grasp point for each object."""
    img = result.plot()
    for obj in analysis:
        if obj["grasp"]:
            gx, gy = obj["grasp"]
            cv2.drawMarker(img, (gx, gy), (0, 255, 255),
                           cv2.MARKER_CROSS, 22, 3)
            cv2.circle(img, (gx, gy), 6, (0, 255, 255), 2)
    return img


def report(analysis, label=""):
    if not analysis:
        print(f"  {label}no objects with masks")
        return
    print(f"  {label}{len(analysis)} object(s):")
    for o in analysis:
        gx, gy = o["grasp"] if o["grasp"] else ("-", "-")
        print(f"    {o['label']:<10} box={o['box_area']:>8.0f}px  "
              f"mask={o['mask_area']:>8.0f}px  "
              f"fill={o['fill']:>4.0%}  grasp=({gx},{gy})")


def self_test():
    import urllib.request

    print("=" * 60)
    print("  Segmentation self-test")
    print("=" * 60)

    model = YOLO(MODEL_NAME)
    print(f"  Model: {MODEL_NAME}  ({len(model.names)} classes, outputs masks)")

    urllib.request.urlretrieve("https://ultralytics.com/images/bus.jpg",
                               "/tmp/seg_sample.jpg")
    img = cv2.imread("/tmp/seg_sample.jpg")
    result = model(img, conf=CONFIDENCE, verbose=False)[0]
    analysis = analyse(result, model)

    print()
    report(analysis)

    if analysis:
        avg_fill = sum(o["fill"] for o in analysis) / len(analysis)
        print(f"\n  On average, only {avg_fill:.0%} of each bounding box is")
        print("  actually the object. The rest is background - which is why a")
        print("  robot arm cannot grasp from a box, and needs the mask.")

    cv2.imwrite("output_segmentation.jpg", annotate(result, analysis))
    print("\n  annotated (masks + grasp points) -> output_segmentation.jpg")
    return 0


def run_image(path):
    model = YOLO(MODEL_NAME)
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read '{path}'")
        return 1
    result = model(img, conf=CONFIDENCE, verbose=False)[0]
    analysis = analyse(result, model)
    print(f"\n{path}:")
    report(analysis)
    cv2.imwrite("output_segmentation.jpg", annotate(result, analysis))
    print("\n  annotated -> output_segmentation.jpg")
    return 0


def open_camera(width=640, height=480, source=None):
    # source can be a camera index (int) or a phone-stream URL (str),
    # e.g. "http://192.168.1.42:8080/video" from an IP-webcam app.
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
    print("from the terminal inside VS Code, or enable your terminal in System")
    print("Settings > Privacy & Security > Camera, then quit (Cmd+Q) and reopen.")
    return None


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())
    if "--image" in sys.argv:
        i = sys.argv.index("--image")
        if i + 1 >= len(sys.argv):
            print("Usage: python segmentation.py --image photo.jpg")
            sys.exit(1)
        sys.exit(run_image(sys.argv[i + 1]))

    model = YOLO(MODEL_NAME)
    source = None
    if "--cam" in sys.argv:
        source = int(sys.argv[sys.argv.index("--cam") + 1])
    elif "--url" in sys.argv:
        source = sys.argv[sys.argv.index("--url") + 1]
    cam = open_camera(source=source)
    if cam is None:
        sys.exit(1)

    print("  The yellow cross is the grasp point. Press Q to quit.\n")
    misses = 0
    while True:
        ok, frame = cam.read()
        if not ok or frame is None:
            misses += 1
            if misses > 30:
                break
            continue
        misses = 0

        result = model(frame, conf=CONFIDENCE, verbose=False)[0]
        analysis = analyse(result, model)
        out = annotate(result, analysis)

        cv2.imshow("Segmentation", out)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
