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

## Lesson 5 - Mutation + elitism (full GA)
- Swap mutation: pick 2 positions, swap their stops. Always stays a valid route. Happens to ~20% of children (MUTATION_RATE).
- Elitism: copy the best 2 routes unchanged into the next generation, so the best answer can never be lost.
- Full loop per generation: elitism -> tournament x2 -> ordered crossover -> maybe mutate -> repeat until 100 routes.
- Result: found the true best (49.4 km) by gen 20. Diversity stayed around 12-20 routes instead of collapsing to 1.
- The route it found is the brute-force route driven backwards: same loop, same km.
- Reliability: 8 of 10 seeds found 49.4 km; 2 got stuck at 50.7 km. A GA gives a very good answer, not a guaranteed perfect one.
- The dials: POP_SIZE, GENERATIONS, TOURNAMENT_K, MUTATION_RATE, ELITE.
- Chart: lesson5_progress.png (best km per generation).

## Lesson 6 - Drawing the route on a map
- folium builds an interactive map (Esri.WorldStreetMap tiles, no key needed; OSM tiles return 403 "Access blocked" when the html is opened as a local file) and saves it as an .html file. Install once: pip install folium
- Red house pin = depot (Albrook). Blue numbered pins = stops, numbered in the order the truck visits them.
- Blue line = GA best route (49.4 km). Gray dashed line = a random route (85.7 km), off by default; switch it on in the corner box.
- route_points() adds the depot at both ends and turns stop numbers into (lat, lon).
- Lines are straight because our distances are straight-line. With road distances they'd follow streets.

## Lesson 7 - Inside Felipe's AnyLogic model (MilkRun2)
- Felipe's files live in anylogic/original/ and are NOT committed (it's his work; see .gitignore).
- Agents: Main (everything), Manufacturer (depot), Supplier (stops), Truck (ONE truck = ONE route = one chromosome).
- Population = 'trucks'. Every generation, every truck actually drives its route on real roads (GIS map, FASTEST routing).
- Fitness = minutes driven (time()-startTime). Lower is better. Real road times, not straight-line km.
- Generation loop (Main.nextGeneration): when all trucks are back -> draw best route -> keep the best populationSize trucks, delete the rest -> make offspring -> send "start".
- Selection: parents picked completely at random. The pressure comes from "survivor selection": parents + children compete, only the best survive (strong elitism).
- Crossover: start with p1's first 2 stops, then alternate parents: "what comes after my last stop in this parent?" If already used, pick a random unused stop.
- Mutation (if it happens): 1/3 swap, 1/3 scramble (shuffle a chunk), 1/3 inversion (reverse a chunk).
- Map is centred on Austin, Texas (30.31, -97.67).
- Python vs AnyLogic: same GA idea, different choices. Ours = tournament + OX + swap + elitism 2, straight-line km.

### Running Felipe's model
- Run A (9 stops, pop 50, 300 gens, mutation 0.2, crossover 0.8): best drops ~290 -> ~227 min by gen ~20, then flat. Same shape as our Python run.
- Run B (his defaults: 15 stops, pop 25, 1000 gens, mutation 0.1): "staircase" - long flat stretches, small drops, last improvement ~gen 690, ends ~268 min. 15 stops = ~1.3 trillion routes, much harder.
- In both, the average line sticks to the best line -> the population is almost all clones. His "keep only the best survivors" squeezes out diversity; progress then waits for lucky mutations (the staircase).
- Our Python kept the average ~3 km above the best (diversity alive) thanks to tournament + only 2 elites.
- His map draws straight lines between stops, but fitness is real road driving time. What you see != what's measured.
