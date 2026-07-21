#!/usr/bin/env bash
#
# AI Robotics Bootcamp - Lesson 23
# Scaffold a professional robotics project.
#
# Creates the folder structure, README.md, .gitignore and requirements.txt
# that every project in this course should start with - so you never again
# begin with loose files in Downloads.
#
# Usage:
#     bash new_project.sh MoveBot
#     bash new_project.sh MoveBot ~/AI-Robotics-Engineer

set -e

NAME="${1:-}"
PARENT="${2:-$PWD}"

if [ -z "$NAME" ]; then
  echo "Usage: bash new_project.sh <ProjectName> [parent-folder]"
  echo "Example: bash new_project.sh MoveBot ~/AI-Robotics-Engineer"
  exit 1
fi

TARGET="$PARENT/$NAME"

if [ -e "$TARGET" ]; then
  # Never silently overwrite someone's existing work.
  echo "'$TARGET' already exists. Choose another name or delete it first."
  exit 1
fi

echo "Creating $TARGET"
mkdir -p "$TARGET"/{src,tests,docs,data,notebooks,assets}

# --- README ----------------------------------------------------------------
cat > "$TARGET/README.md" <<EOF
# $NAME

## Objective

_One sentence: what does this robot or program do?_

## Skills used

- Python
- (add: OpenCV, Webots, ROS 2 ...)

## Setup

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

## Run

\`\`\`bash
python src/main.py
\`\`\`

## Project structure

\`\`\`text
$NAME/
├── src/         source code
├── tests/       tests
├── docs/        notes and diagrams
├── data/        datasets (not committed)
├── notebooks/   experiments
└── assets/      images, models
\`\`\`

## Status

Work in progress.
EOF

# --- .gitignore ------------------------------------------------------------
cat > "$TARGET/.gitignore" <<'EOF'
# Python
__pycache__/
*.pyc
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# macOS
.DS_Store

# Secrets - never commit these
.env
*.key

# Data and outputs
data/
output/
EOF

# --- requirements.txt ------------------------------------------------------
cat > "$TARGET/requirements.txt" <<'EOF'
numpy
matplotlib
opencv-python
EOF

# --- a starter source file -------------------------------------------------
cat > "$TARGET/src/main.py" <<EOF
"""$NAME - entry point."""


def main():
    print("$NAME is running")


if __name__ == "__main__":
    main()
EOF

# Git keeps track of files, not folders, so empty ones would vanish.
for d in tests docs data notebooks assets; do
  touch "$TARGET/$d/.gitkeep"
done

echo ""
echo "Created:"
echo "  $NAME/"
echo "  ├── README.md          project documentation"
echo "  ├── .gitignore         keeps secrets and junk out of Git"
echo "  ├── requirements.txt   reproducible dependencies"
echo "  ├── src/main.py        starter code"
echo "  └── tests/ docs/ data/ notebooks/ assets/"
echo ""
echo "Next steps:"
echo "  cd \"$TARGET\""
echo "  python3 -m venv .venv && source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  git init && git add . && git commit -m \"Start $NAME\""
echo ""
