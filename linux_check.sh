#!/usr/bin/env bash
#
# AI Robotics Bootcamp - Lesson 18
# Which Linux commands work on this machine?
#
# macOS and Linux are both UNIX-like, so most commands are shared - but not
# all, and some behave differently. This script tells you exactly where you
# stand before you move to Ubuntu or a Jetson.
#
# Run with:
#     bash linux_check.sh

echo "======================================================"
echo "  Linux command check"
echo "======================================================"
echo "  System: $(uname -s) $(uname -r) ($(uname -m))"
echo "------------------------------------------------------"

# Commands every robotics engineer uses daily.
CORE="pwd ls cd clear whoami date cal mkdir rmdir cp mv rm grep find man chmod ps kill df du"
# Commands that are commonly missing on macOS.
EXTRA="tree htop wget xdg-open"
# The toolchain.
TOOLS="python3 pip3 git curl nano vim"

check_group() {
  local title="$1"; shift
  echo ""
  echo "  $title"
  local missing=""
  for c in $1; do
    if command -v "$c" >/dev/null 2>&1; then
      printf "    [x] %s\n" "$c"
    else
      printf "    [ ] %s  (not installed)\n" "$c"
      missing="$missing $c"
    fi
  done
  echo "$missing" > /tmp/_missing_$$
}

check_group "Core commands (shared by macOS and Linux):" "$CORE"
check_group "Often missing on macOS:" "$EXTRA"
MISSING_EXTRA=$(cat /tmp/_missing_$$ 2>/dev/null)
check_group "Development tools:" "$TOOLS"
rm -f /tmp/_missing_$$

echo ""
echo "------------------------------------------------------"
echo "  Same name, different behaviour"
echo "------------------------------------------------------"
echo ""
echo "  These exist on both systems but take DIFFERENT options,"
echo "  because macOS uses BSD tools and Linux uses GNU tools:"
echo ""
echo "    sed -i        Linux: sed -i 's/a/b/' f.txt"
echo "                  macOS: sed -i '' 's/a/b/' f.txt   <- needs ''"
echo ""
echo "    date          Linux: date -d '2026-01-01'"
echo "                  macOS: date -v +1d"
echo ""
echo "    stat          Linux: stat -c %s file"
echo "                  macOS: stat -f %z file"
echo ""
echo "    ls colour     Linux: ls --color=auto"
echo "                  macOS: ls -G"
echo ""

if [ -n "$MISSING_EXTRA" ]; then
  echo "------------------------------------------------------"
  echo "  To install the missing ones (optional):"
  echo "      brew install$MISSING_EXTRA"
  echo "------------------------------------------------------"
fi

echo ""
echo "  Scripts written on macOS can fail on a Jetson, and vice"
echo "  versa. When that happens, this list is the first place"
echo "  to look."
echo ""
