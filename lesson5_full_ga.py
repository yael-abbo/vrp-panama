"""
Lesson 5: Mutation + elitism = a complete genetic algorithm.

Each generation:
  1. Elitism:   copy the best ELITE routes straight into the next generation.
  2. Selection: pick two parents with a tournament.
  3. Crossover: make a child with ordered crossover.
  4. Mutation:  with probability MUTATION_RATE, swap two stops in the child.
  Repeat 2-4 until the new population is full.
"""
import random

from lesson2_chromosome import random_route, route_length, show
from lesson3_selection import tournament, unique_routes
from lesson4_crossover import ordered_crossover

# --- Settings (the "dials" of the GA) ------------------------------------
POP_SIZE = 100        # routes per generation
GENERATIONS = 100     # how many rounds of evolution
TOURNAMENT_K = 3      # tournament size (lesson 3)
MUTATION_RATE = 0.2   # chance that a child gets a swap
ELITE = 2             # best routes copied unchanged each generation


def swap_mutation(route):
    """Pick two positions at random and swap their stops. Still a valid route."""
    route = route[:]                         # work on a copy, don't change the original
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]
    return route


def genetic_algorithm(seed=42, mutation_rate=MUTATION_RATE, elite=ELITE, verbose=True):
    random.seed(seed)
    population = [random_route() for _ in range(POP_SIZE)]
    history = []                             # best length per generation, for the chart

    for gen in range(GENERATIONS + 1):
        population.sort(key=route_length)    # shortest first
        best = population[0]
        history.append(route_length(best))
        if verbose and gen % 10 == 0:
            avg = sum(route_length(r) for r in population) / POP_SIZE
            print(f"  gen {gen:3d}: different routes = {unique_routes(population):3d}   "
                  f"average = {avg:5.1f} km   best = {route_length(best):5.1f} km")
        if gen == GENERATIONS:
            break

        next_gen = population[:elite]        # 1. elitism
        while len(next_gen) < POP_SIZE:
            mom = tournament(population, TOURNAMENT_K)       # 2. selection
            dad = tournament(population, TOURNAMENT_K)
            child = ordered_crossover(mom, dad)              # 3. crossover
            if random.random() < mutation_rate:              # 4. mutation
                child = swap_mutation(child)
            next_gen.append(child)
        population = next_gen

    return best, history


if __name__ == "__main__":
    print("Full GA (elitism + selection + crossover + mutation):")
    best, history = genetic_algorithm()
    print(f"\nBest route: {route_length(best):.1f} km  (true best is 49.4 km)")
    print(" ", show(best))

    # How reliable is it? Run it 10 times with different seeds.
    print("\n10 runs with different seeds:")
    results = [route_length(genetic_algorithm(seed=s, verbose=False)[0]) for s in range(10)]
    print("  ", [round(r, 1) for r in results])
    print(f"  found the true best (49.4 km) in {sum(r < 49.45 for r in results)} of 10 runs")

    # Chart: best route length per generation
    try:
        import matplotlib.pyplot as plt
        plt.plot(history)
        plt.axhline(49.4, linestyle="--", color="gray", label="true best (49.4 km)")
        plt.xlabel("Generation")
        plt.ylabel("Best route length (km)")
        plt.title("GA progress - Panama City route")
        plt.legend()
        plt.savefig("lesson5_progress.png", dpi=120, bbox_inches="tight")
        print("\nSaved chart: lesson5_progress.png")
    except ImportError:
        print("\n(matplotlib not installed - skipping the chart)")
