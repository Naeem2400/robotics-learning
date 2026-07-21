#!/usr/bin/env bash
#
# AI Robotics Bootcamp - Lesson 19
# Practise Git safely.
#
# This builds a THROWAWAY repository in a temporary folder, runs the whole
# workflow (init -> add -> commit -> branch -> merge -> log), shows you the
# real output of every step, then deletes it.
#
# Your actual project is never touched, so you cannot break anything.
#
# Run with:
#     bash git_practice.sh

set -e

SANDBOX=$(mktemp -d)
trap 'rm -rf "$SANDBOX"' EXIT      # always clean up, even on error

step() {
  echo ""
  echo "======================================================"
  echo "  $1"
  echo "======================================================"
}

run() {
  echo ""
  echo "\$ $*"
  "$@"
}

cd "$SANDBOX"

echo "Practice repository: $SANDBOX"
echo "(it will be deleted automatically when this finishes)"

# ---------------------------------------------------------------------------
step "1. git init - start tracking a project"
run git init -q
run ls -a
echo ""
echo "  The .git folder is Git's brain. Never edit it by hand."

# ---------------------------------------------------------------------------
step "2. git status - what does Git know?"
echo "robot_name = 'NaeemBot'" > robot.py
run git status --short
echo ""
echo "  '??' means UNTRACKED: Git can see robot.py but is not watching it."

# ---------------------------------------------------------------------------
step "3. git add - start watching the file"
run git add robot.py
run git status --short
echo ""
echo "  'A' means ADDED: the file is staged, ready to be saved."

# ---------------------------------------------------------------------------
step "4. git commit - save a snapshot"
git -c user.name="Practice" -c user.email="practice@example.com" \
    commit -q -m "First robot project"
echo ""
echo "\$ git commit -m \"First robot project\""
run git log --oneline

# ---------------------------------------------------------------------------
step "5. Make a change and commit again"
echo "battery = 100" >> robot.py
run git status --short
echo ""
echo "  'M' means MODIFIED: a tracked file changed."
git add robot.py
git -c user.name="Practice" -c user.email="practice@example.com" \
    commit -q -m "Add battery level"
run git log --oneline

# ---------------------------------------------------------------------------
step "6. git branch - work without breaking main"
run git branch voice-feature
run git checkout -q voice-feature
echo "voice = 'Hello human'" >> robot.py
git add robot.py
git -c user.name="Practice" -c user.email="practice@example.com" \
    commit -q -m "Add voice output"
run git log --oneline
echo ""
echo "  This branch has 3 commits. Now look at main:"
run git checkout -q main
run git log --oneline
echo ""
echo "  main still has 2. The voice work is isolated - main never broke."
run cat robot.py

# ---------------------------------------------------------------------------
step "7. git merge - bring the work back"
run git merge -q voice-feature
run git log --oneline
run cat robot.py
echo ""
echo "  The voice line is now in main."

# ---------------------------------------------------------------------------
step "8. Going back in time"
FIRST=$(git rev-list --max-parents=0 HEAD)
echo ""
echo "\$ git show $FIRST --stat"
git show "$FIRST" --stat --oneline | head -5
echo ""
echo "  Every old version is still there. Nothing is ever really lost."

# ---------------------------------------------------------------------------
echo ""
echo "======================================================"
echo "  Done - the practice folder is now deleted."
echo "======================================================"
echo ""
echo "  You just ran the exact workflow used by every robotics"
echo "  company: init, add, commit, branch, merge."
echo ""
