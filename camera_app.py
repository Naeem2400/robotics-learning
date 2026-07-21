"""
AI Robotics Bootcamp - Lesson 30
Your first computer vision program: live camera, photos, and video.

This is the mini challenge, solved:

    C  capture a photo
    R  start recording
    T  stop recording
    Q  quit

Usage:
    python camera_app.py            # live window
    python camera_app.py --test     # grab ONE frame and exit (no window)

The --test mode is useful for checking the camera works on a machine with
no display, or before granting the app permission to show windows.

Captured photos and videos are saved into captures/ which is git-ignored -
never commit camera footage to a public repository.
"""

import os
import sys

try:
    import cv2
except ImportError:
    print("OpenCV is not installed in this environment.\n")
    print("    python3.13 -m venv .venv")
    print("    source .venv/bin/activate")
    print("    pip install opencv-python\n")
    sys.exit(1)

OUTPUT_DIR = "captures"
FPS = 20.0


def open_camera():
    """Try camera 0, then 1, then 2. Returns the capture or None.

    On macOS the FIRST time any program opens the camera, the system shows a
    permission prompt. If it is denied, read() returns empty frames with NO
    error message - which is why we test a real frame here rather than
    trusting isOpened().
    """
    for index in (0, 1, 2):
        camera = cv2.VideoCapture(index)
        if camera.isOpened():
            success, frame = camera.read()
            if success and frame is not None:
                print(f"Camera {index} opened: "
                      f"{frame.shape[1]} x {frame.shape[0]} pixels")
                return camera
            camera.release()
            print(f"Camera {index} opened but returned no frame "
                  f"(permission denied, or another app is using it)")

    print("\nNo working camera found. Check:")
    print("  - System Settings > Privacy & Security > Camera")
    print("  - Close Zoom / Teams / FaceTime, which may hold the camera")
    return None


def self_test():
    """Grab a single frame and report. No window, no saved image."""
    print("=" * 54)
    print("  Camera self-test")
    print("=" * 54)

    camera = open_camera()
    if camera is None:
        return 1

    success, frame = camera.read()
    camera.release()

    if not success or frame is None:
        print("Could not read a frame.")
        return 1

    height, width, channels = frame.shape
    print(f"  Frame size : {width} x {height}")
    print(f"  Channels   : {channels} (blue, green, red - OpenCV uses BGR)")
    print(f"  Data type  : {frame.dtype}")
    print(f"  Numbers    : {width * height * channels:,} per frame")
    print(f"  At {FPS:.0f} fps that is "
          f"{width * height * channels * FPS / 1_000_000:.0f} million "
          f"numbers per second.")
    print("\n  Camera works. Run without --test for the live window.")
    return 0


def main():
    if "--test" in sys.argv:
        sys.exit(self_test())

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    camera = open_camera()
    if camera is None:
        sys.exit(1)

    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = None
    photo_count = 0

    print("\n  C = capture photo   R = start recording")
    print("  T = stop recording  Q = quit\n")

    while True:
        success, frame = camera.read()
        if not success:
            print("Lost the camera feed.")
            break

        # Show the user what state we are in, drawn onto the frame itself.
        label = "RECORDING" if writer else "live"
        colour = (0, 0, 255) if writer else (0, 200, 0)
        cv2.putText(frame, label, (12, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)

        if writer is not None:
            writer.write(frame)

        cv2.imshow("Robot Camera", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            path = f"{OUTPUT_DIR}/photo_{photo_count:03d}.jpg"
            cv2.imwrite(path, frame)
            print(f"  saved {path}")
            photo_count += 1

        elif key == ord("r"):
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                path = f"{OUTPUT_DIR}/video.mp4"
                # The size here MUST match the frame size or the file will
                # be created but stay empty - a classic silent failure.
                writer = cv2.VideoWriter(path, fourcc, FPS, (width, height))
                print(f"  recording to {path}")
            else:
                print("  already recording")

        elif key == ord("t"):
            if writer is not None:
                writer.release()
                writer = None
                print("  recording stopped")
            else:
                print("  not recording")

        elif key == ord("q"):
            break

    if writer is not None:
        writer.release()
    camera.release()
    cv2.destroyAllWindows()
    print("\n  Camera released. Goodbye.")


if __name__ == "__main__":
    main()
