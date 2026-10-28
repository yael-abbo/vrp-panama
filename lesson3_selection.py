"""
Lesson 3: Selection - choosing which routes get to be parents.

Two ways to choose:
  1. "Only the best": always take the top 10 routes.
  2. Tournament: pick a few routes at random, the best of that small group wins.

We have no crossover or mutation yet, so parents are simply copied into
the next generation. That lets us watch ONE thing: how fast each method
loses variety (diversity) in the population.
"""
import random

from lesson2_chromosome import random_route, route_length

POP_SIZE = 100


def select_top(population, k=10):
    """'Only the best': every parent comes from the top k routes."""
    top = sorted(population, key=route_length)[:k]
    return random.choice(top)


def tournament(population, k=3):
    """Pick k routes at random. The shortest of those k wins."""
    contestants = random.sample(population, k)
    return min(contestants, key=route_length)


def unique_routes(population):
    """How many different routes are left? (a simple measure of diversity)"""
    return len({tuple(r) for r in population})


def run(select, generations=8):
    random.seed(42)
    population = [random_route() for _ in range(POP_SIZE)]
    for gen in range(generations + 1):
        lengths = [route_length(r) for r in population]
        print(f"  gen {gen}: different routes = {unique_routes(population):3d}   "
              f"average = {sum(lengths) / len(lengths):5.1f} km   best = {min(lengths):5.1f} km")
        # next generation = POP_SIZE parents chosen by the selection method
        population = [select(population) for _ in range(POP_SIZE)]


if __name__ == "__main__":
       for k in [2, 3, 10]:
        print(f"\nTournament of {k}:")
        run(lambda pop: tournament(pop, k=k))