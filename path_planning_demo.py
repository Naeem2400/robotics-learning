"""
AI Robotics Bootcamp - Lesson 28
Path planning: Dijkstra vs A* on the same map.

Everyone is told "A* is faster than Dijkstra because it uses a heuristic."
This script proves it. Both algorithms run on the same grid, find paths of
the SAME length, and the script counts how many cells each had to examine.

Needs no libraries.

Run with:
    python3 path_planning_demo.py
"""

import heapq

# S = start, G = goal, # = obstacle, . = free space
GRID = [
    "S.........#..........",
    "..........#..........",
    "....####..#..####....",
    "....#..#..#..#..#....",
    "....#..#.....#..#....",
    "....#..#######..#....",
    "....#...........#....",
    "....#############....",
    ".....................",
    "..........#..........",
    "..........#.........G",
]

HEIGHT = len(GRID)
WIDTH = len(GRID[0])

MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]      # right, left, down, up


def find(symbol):
    for y, row in enumerate(GRID):
        x = row.find(symbol)
        if x != -1:
            return (y, x)
    raise ValueError(f"'{symbol}' not found in the grid")


def walkable(y, x):
    return 0 <= y < HEIGHT and 0 <= x < WIDTH and GRID[y][x] != "#"


def heuristic(a, b):
    """Manhattan distance - our guess at the remaining cost.

    This is what makes A* different. It must never OVERESTIMATE the true
    remaining distance, or A* can return a non-optimal path. With 4-way
    movement, Manhattan distance is exactly right.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def search(start, goal, use_heuristic):
    """Dijkstra when use_heuristic is False, A* when it is True.

    They are the SAME algorithm. The only difference is what decides which
    cell to look at next:
        Dijkstra: cost so far
        A*:       cost so far + estimated cost remaining
    """
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()

    while frontier:
        _priority, current = heapq.heappop(frontier)

        if current in explored:
            continue
        explored.add(current)

        if current == goal:
            break

        y, x = current
        for dy, dx in MOVES:
            neighbour = (y + dy, x + dx)
            if not walkable(*neighbour):
                continue

            new_cost = cost_so_far[current] + 1
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                priority = new_cost
                if use_heuristic:
                    priority += heuristic(neighbour, goal)
                heapq.heappush(frontier, (priority, neighbour))
                came_from[neighbour] = current

    # Walk backwards from the goal to rebuild the path.
    if goal not in came_from:
        return None, explored

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path, explored


def render(path, explored, title):
    print(f"  {title}")
    print("    (o = cells the algorithm examined, * = the path it chose)\n")

    path_set = set(path or [])
    for y, row in enumerate(GRID):
        line = ""
        for x, cell in enumerate(row):
            here = (y, x)
            if cell in "SG":
                line += cell
            elif here in path_set:
                line += "*"
            elif here in explored:
                line += "o"
            elif cell == "#":
                line += "#"
            else:
                line += "."
        print("    " + line)
    print()


def main():
    start = find("S")
    goal = find("G")

    print("=" * 62)
    print("  Lesson 28 - Path planning: Dijkstra vs A*")
    print("=" * 62)
    print()
    print("  The map (# = obstacle):\n")
    for row in GRID:
        print("    " + row)
    print()

    results = {}
    for name, use_heuristic in [("Dijkstra", False), ("A*", True)]:
        print("-" * 62)
        path, explored = search(start, goal, use_heuristic)
        render(path, explored, f"{name}:")

        steps = len(path) - 1 if path else None
        results[name] = (steps, len(explored))
        print(f"    path length : {steps} steps")
        print(f"    cells examined: {len(explored)}")
        print()

    # ---- the comparison -------------------------------------------------
    d_steps, d_explored = results["Dijkstra"]
    a_steps, a_explored = results["A*"]

    print("=" * 62)
    print("  What just happened")
    print("=" * 62)
    print()
    print(f"    {'':<12}{'path':>8}{'examined':>12}")
    print(f"    {'Dijkstra':<12}{d_steps:>8}{d_explored:>12}")
    print(f"    {'A*':<12}{a_steps:>8}{a_explored:>12}")
    print()

    if d_steps == a_steps:
        print("  Both found a path of the SAME length - both are optimal.")
    saved = d_explored - a_explored
    if saved > 0:
        pct = 100.0 * saved / d_explored
        print(f"  But A* examined {saved} fewer cells ({pct:.0f}% less work),")
        print("  because its heuristic pulled the search toward the goal")
        print("  instead of spreading out evenly in all directions.")
    print()
    print("  Look at the two maps above: Dijkstra's 'o' cells fan out in a")
    print("  circle around the start. A*'s stretch toward the goal.")
    print()
    print("  Same answer, less work. That is the whole point of A*.")


if __name__ == "__main__":
    main()
