# Lesson notes

## Lesson 1 - The problem
- One truck, a depot in Albrook, 9 stops. Visit each once, come back. Shortest total distance wins.
- One truck = Traveling Salesman Problem. Several trucks = Vehicle Routing Problem.
- Trying every order doesn't scale: 9 stops = 362,880 routes, 20 stops = ~2.4 quintillion.
- A GA "breeds" good routes instead: random routes -> keep the short ones -> combine them -> small random changes -> repeat.
- Stops are now specific landmarks (malls, parks, hospitals, a stadium, the airport) with exact coordinates from Google Maps.
- Distances are straight-line (haversine) for now. Real road distances come later.
- Question for next time: how would you write one route as a Python list?

## Lesson 2 - Chromosome and fitness
- A route (chromosome) is a list of stop numbers, e.g. [3, 1, 7, 2, 9, 5, 4, 8, 6]. Each number appears exactly once.
- The depot (0) is left out of the list: the truck always starts and ends there, so the GA shouldn't be able to move it.
- Distance table: calculate every pair once, then just look it up (dist[i][j]).
- Fitness = total km (depot -> stops in order -> depot). Lower is better.
- random.seed(42) makes "random" results repeat, so runs can be compared.
- 100 random routes: best 55.9 km, worst 118.6 km. Order matters a lot.
- True best route (checked all 362,880 by brute force): 49.4 km. This is the target for our GA.

## Lesson 3 - Selection
- Selection = choosing which routes become parents. Better routes should win more often, but not always.
- "Only the best" (top 10): diversity collapses to 1 route by generation 3. Stuck at 55.9 km forever.
- Tournament (pick 3 at random, best of the 3 wins): collapses too, but slower (gen 5). Weaker routes still sometimes get picked.
- Selection alone can never find a better route than the best one we started with. It only copies. New routes come from crossover (L4) and mutation (L5).
- Diversity = how many different routes are in the population. Losing it too early = "premature convergence": the GA gets stuck on a so-so answer.
- Tournament size k is a dial: bigger k = pickier = faster but less diverse.

## Lesson 4 - Crossover
- Naive crossover (first half of A + second half of B) gives [1,2,3,4,5,4,3,2,1]: repeats 1-4, skips 6-9. Not a valid route.
- Ordered crossover (OX): copy a slice of A into the same spots, then fill the gaps left to right with B's stops in B's order, skipping ones already used. Always valid.
- The child keeps a chunk of A's route exactly and B's general order for the rest.
- GA with selection + OX: 55.9 -> 49.9 km by gen 10. First time we beat the best random route. Crossover creates new routes.
- But: it found 49.9 at gen 10 and then LOST it (gen 15 = 50.7). Nothing protects the best route. Fix: elitism (L5).
- And: all 100 routes became clones by gen 15, stuck at 50.7. Nothing adds new variety. Fix: mutation (L5).
