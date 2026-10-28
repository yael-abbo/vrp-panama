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
