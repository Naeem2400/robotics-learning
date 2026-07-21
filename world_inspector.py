"""
AI Robotics Bootcamp - Lesson 24
Read a Webots world file and print its Scene Tree.

The Scene Tree panel in Webots shows the objects in your world. That panel
is just a view of a plain text file. This script reads a .wbt file and
prints the same structure, so you can see that a "3D world" is really a
list of nodes with fields.

Needs no libraries and no Webots.

Usage:
    python3 world_inspector.py worlds/movebot.wbt
    python3 world_inspector.py                     # lists all worlds
"""

import os
import re
import sys

WORLDS_DIR = "worlds"

# A node line looks like:  E-puck {   or   RectangleArena {
NODE_RE = re.compile(r"^(\s*)([A-Za-z][\w\-]*)\s*\{")
# A field line looks like:  translation -0.6 -0.6 0
FIELD_RE = re.compile(r"^(\s*)([a-z][\w]*)\s+(.+?)\s*$")

# Fields worth showing - the rest is mostly noise for a beginner.
INTERESTING = {
    "translation", "rotation", "controller", "name", "floorSize",
    "size", "wallHeight", "title", "basicTimeStep",
}


def inspect(path):
    if not os.path.exists(path):
        print(f"No such file: {path}")
        return

    print("=" * 62)
    print(f"  Scene Tree of {path}")
    print("=" * 62)

    externprotos = []
    nodes = 0

    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\n")

            # Webots downloads these object definitions from the internet.
            if stripped.startswith("EXTERNPROTO"):
                name = stripped.split("/")[-1].replace('.proto"', "")
                externprotos.append(name)
                continue

            # Hidden fields are simulation state Webots saves automatically.
            if "hidden" in stripped:
                continue

            node = NODE_RE.match(stripped)
            if node:
                indent, node_name = node.group(1), node.group(2)
                depth = len(indent) // 2
                print(f"  {'  ' * depth}+ {node_name}")
                nodes += 1
                continue

            field = FIELD_RE.match(stripped)
            if field:
                indent, key, value = field.groups()
                if key in INTERESTING:
                    depth = len(indent) // 2
                    if len(value) > 42:
                        value = value[:42] + " ..."
                    print(f"  {'  ' * depth}    {key}: {value}")

    print("-" * 62)
    print(f"  {nodes} nodes")
    if externprotos:
        print(f"  {len(externprotos)} object definitions downloaded from GitHub:")
        print(f"     {', '.join(externprotos[:6])}"
              + (" ..." if len(externprotos) > 6 else ""))
    print("-" * 62)
    print()
    print("  Every object in the 3D view is a NODE.")
    print("  Everything indented under it is a FIELD of that node.")
    print("  Editing this text file and editing the Scene Tree in Webots")
    print("  are the same thing.")


def list_worlds():
    if not os.path.isdir(WORLDS_DIR):
        print(f"No '{WORLDS_DIR}' folder here. Run this from the project root.")
        return

    worlds = sorted(w for w in os.listdir(WORLDS_DIR) if w.endswith(".wbt"))
    print("Worlds in this project:\n")
    for w in worlds:
        print(f"  python3 world_inspector.py {WORLDS_DIR}/{w}")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect(sys.argv[1])
    else:
        list_worlds()
