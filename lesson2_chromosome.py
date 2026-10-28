"""
Lesson 2: Turning a route into a chromosome, and giving it a score.

- A route is a list of stop numbers, e.g. [3, 1, 7, 2, 9, 5, 4, 8, 6].
- The depot (number 0) is NOT in the list. The truck always starts and
  ends there, so the GA never needs to move it.
- The score (fitness) of a route is its total length in km. Shorter is better.
"""
import random

from lesson1_setup import stops, distance_km

names = list(stops)            # names[0] is the depot
N = len(names)                 # 10 places in total (depot + 9 stops)

# --- Step 1: a distance table -------------------------------------------
# We will measure the same pairs of places thousands of times, so we
# calculate every pair once and look it up later. dist[i][j] = km from i to j.
dist = [[distance_km(stops[names[i]], stops[names[j]]) for j in range(N)]
        for i in range(N)]


# --- Step 2: the chromosome ---------------------------------------------
def random_route():
    """A random order of the stops 1..9. Each stop appears exactly once."""
    return random.sample(range(1, N), N - 1)


# --- Step 3: the fitness (score) ----------------------------------------
def route_length(route):
    """Total km: depot -> every stop in order -> back to depot."""
    total = dist[0][route[0]]                  # leave the depot
    for a, b in zip(route, route[1:]):         # stop to stop
        total += dist[a][b]
    total += dist[route[-1]][0]                # drive back to the depot
    return total


def show(route):
    """Turn a list of numbers back into place names, so humans can read it."""
    return " -> ".join(["Albrook"] + [names[i].split(" (")[0] for i in route] + ["Albrook"])


if __name__ == "__main__":
    random.seed(42)   # makes the "random" results the same every time you run it

    # The order the stops happen to be written in lesson 1
    in_order = list(range(1, N))
    print("Route in list order:", in_order)
    print(f"  length: {route_length(in_order):.1f} km\n")

    # Five random routes and their scores
    print("Five random routes:")
    for _ in range(5):
        r = random_route()
        print(f"  {r}  ->  {route_length(r):5.1f} km")

    # A whole population: 100 random routes
    population = [random_route() for _ in range(100)]
    population.sort(key=route_length)          # shortest first
    best, worst = population[0], population[-1]
    print(f"\nOut of 100 random routes:")
    print(f"  best : {route_length(best):5.1f} km   {best}")
    print(f"  worst: {route_length(worst):5.1f} km   {worst}")
    print(f"\nBest route in plain words:\n  {show(best)}")
