"""
Mini Challenge - Battery check

If the battery is below 20%, the robot must stop working and go and charge.
Otherwise it keeps working.

Run with:
    python3 challenge_solution.py
"""

battery = 15   # percent

if battery < 20:
    print("Battery low")
    print("Go charging")
else:
    print("Keep working")
