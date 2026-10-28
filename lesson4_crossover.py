"""
Lesson 4: Crossover - making a child route from two parent routes.

The naive way (first half of A + second half of B) breaks the rule
"every stop appears exactly once". Ordered crossover (OX) fixes that:
  1. Copy a random slice from parent A into the child, in the same spots.
  2. Fill the empty spots, left to right, with parent B's stops in B's
     order, skipping any stop the child already has.
"""
import random

from lesson2_chromosome import random_route, route_length, show
from lesson3_selection import tournament, unique_routes

POP_SIZE = 100


def naive_crossover(a, b):
    """The 'obvious' way. Broken on purpose, to show the problem."""
    half = len(a) // 2
    return a[:half] + b[half:]


def ordered_crossover(a, b, start=None, end=None):
    """OX: keep a slice of A, fill the rest in B's order. Always valid."""
    n = len(a)
    if start is None:                       # pick a random slice
        start, end = sorted(random.sample(range(n + 1), 2))
    child = [None] * n
    child[start:end] = a[start:end]         # step 1: copy the slice from A
    taken = set(child[start:end])
    fill = [stop for stop in b if stop not in taken]   # B's order, minus the slice
    for i in range(n):                      # step 2: fill the gaps left to right
        if child[i] is None:
            child[i] = fill.pop(0)
    return child


def is_valid(route, n_stops=9):
    """True if every stop 1..n_stops appears exactly once."""
    return sorted(route) == list(range(1, n_stops + 1))


def run_ga(generations=50, k=3):
    """Selection + crossover. Still NO mutation - that's lesson 5."""
    random.seed(42)
    population = [random_route() for _ in range(POP_SIZE)]
    for gen in range(generations + 1):
        if gen % 5 == 0:
            lengths = [route_length(r) for r in population]
            print(f"  gen {gen:2d}: different routes = {unique_routes(population):3d}   "
                  f"average = {sum(lengths) / len(lengths):5.1f} km   best = {min(lengths):5.1f} km")
        population = [ordered_crossover(tournament(population, k), tournament(population, k))
                      for _ in range(POP_SIZE)]
    return min(population, key=route_length)


if __name__ == "__main__":
    A = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    B = [9, 8, 7, 6, 5, 4, 3, 2, 1]

    bad = naive_crossover(A, B)
    print("Naive child:  ", bad, " valid?", is_valid(bad))

    good = ordered_crossover(A, B, start=3, end=6)    # fixed slice so you can follow it
    print("OX child:     ", good, " valid?", is_valid(good))

    print("\nGA with selection + ordered crossover (no mutation yet):")
    best = run_ga()
    print(f"\nBest route found: {route_length(best):.1f} km  (true best is 49.4 km)")
    print(" ", show(best))
