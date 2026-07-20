"""
AI Robotics Bootcamp - Environment Checker (Lesson 8)

Checks every layer of the professional robotics toolchain:

    VS Code -> Git -> Python -> ROS 2 -> Simulation

Tools not installed yet are reported as "not installed", not as errors.
You install them as the bootcamp progresses.

Run with:
    python3 setup_check.py
"""

import platform
import shutil
import subprocess
import sys

# (display name, executable, version flag, which lesson introduces it)
TOOLS = [
    ("Python",   sys.executable, "--version", "Module 4"),
    ("VS Code",  "code",         "--version", "Lesson 8"),
    ("Git",      "git",          "--version", "Lesson 8"),
    ("Homebrew", "brew",         "--version", "Lesson 9"),
    ("Docker",   "docker",       "--version", "Lesson 9"),
    ("Webots",   "webots",       "--version", "Lesson 9"),
]


def get_version(executable, flag):
    """Return the tool's first version line, or None if it is not installed."""
    path = shutil.which(executable)
    if path is None:
        return None

    try:
        result = subprocess.run(
            [path, flag],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, OSError):
        return "installed (version check failed)"

    output = result.stdout.strip() or result.stderr.strip()
    return output.splitlines()[0] if output else "installed"


def main():
    print("=" * 58)
    print("  AI Robotics Bootcamp - Environment Check")
    print("=" * 58)
    print(f"  System: {platform.system()} {platform.release()} ({platform.machine()})")
    print("-" * 58)

    missing = []

    for name, executable, flag, lesson in TOOLS:
        version = get_version(executable, flag)

        if version is None:
            print(f"  [ ] {name:<9} not installed          (needed: {lesson})")
            missing.append((name, lesson))
        else:
            print(f"  [x] {name:<9} {version}")

    print("-" * 58)

    if not missing:
        print("  All tools ready. You are set up like a professional. ")
    else:
        print(f"  {len(missing)} tool(s) still to install:")
        for name, lesson in missing:
            print(f"      - {name}  (covered in {lesson})")
        print("\n  This is expected - install them as the bootcamp continues.")

    print("=" * 58)


if __name__ == "__main__":
    main()
