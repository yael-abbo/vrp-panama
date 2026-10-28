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

## Lesson 8 - My own AnyLogic model (anylogic/panama_vrp/PanamaVRP)
- New model PanamaVRP, time unit = minutes.
- GIS Map centred on 9.01, -79.48 (Panama City), scale 150000 ("Center and scale" section). Routing = Straight lines for now.
- Agent types: Depot (single agent 'depot'), Stop (population 'stops', parameters stopName, lat, lon - order matters for add_stops()).
- Stop "On startup": jumpTo(lat, lon);   Main "On startup": depot.jumpTo(...) + nine add_stops(name, lat, lon) calls.
- Java needs ";" at the end of every statement (Python doesn't). Error msg: top line = what, first "at" line = where.
- Opening/zooming the map in the editor is awkward; it's easier to set lat/lon/scale in "Center and scale".

## Lesson 9 - One truck drives one route
- Truck agent: variables route (ArrayList<Integer>), nextIndex, startTime, fitness. Speed 40 km/h (placeholder, so minutes = km x 1.5).
- startTrip(): setLocation(depot), startTime = time(), moveTo(first stop).
- "On arrival to target location": next stop -> or home -> or (if home) fitness = time() - startTime; traceln(...).
- AnyLogic stops are 0-8 (population index); Python stops are 1-9 (depot = 0). Add 1 to compare.
- Random route: list 0..8 + Collections.shuffle(r, getDefaultRandomGenerator()) (AnyLogic's seeded random = like random.seed).
- Check: route [3,4,1,7,5,8,2,6,0] took 149.6 min in AnyLogic. Python says 99.9 km = 149.9 min. 0.2% apart - AnyLogic measures distance on the globe slightly differently than haversine. AnyLogic and Python agree.
- Constant speed doesn't change which route is best; with real roads (different speeds) it will.
- zsh (%) vs Python (>>>): Python code goes in python3 or python3 -c "...".

## Lesson 10 - The GA in AnyLogic
- Main: parameters POP_SIZE 50, GENERATIONS 100, TOURNAMENT_K 3, MUTATION_RATE 0.2, ELITE 2; variables generation, trucksHome, bestFitness, bestRoute.
- Functions: randomRoute, tournament, orderedCrossover, swapMutation, startGeneration, truckFinished, nextGeneration (same pieces as Python lessons 2-5).
- Each truck calls main.truckFinished() when home; the LAST one triggers nextGeneration().
- Build ALL new routes first, then hand them out (tournaments need the old routes).
- "Constructor Main(...) is undefined" = Main didn't compile because of mistakes inside it. Check the Problems panel.
- Gotcha: the Arguments "Type" cell only shows the first line - pasted code was hiding in it.
- 10-gen test: 103 -> 77.8 min. Python confirms that route = 51.96 km = 77.9 min.
- 100-gen run: stuck at 76.02 min from gen 14 to 100. That's the same 50.7 km route Python got stuck on in 2 of 10 runs.
  Stuck:   Albrook -> Costa del Este -> Rommel -> Tocumen -> Pedregal -> Los Andes -> USMA -> Urraca -> Hospital -> Casco (50.74 km)
  Best:    Albrook -> USMA -> Los Andes -> Pedregal -> Tocumen -> Rommel -> Costa del Este -> Urraca -> Hospital -> Casco (49.36 km)
- = a LOCAL OPTIMUM: to fix it you must reverse the first 6 stops. Every single swap makes it worse (best swap = 51.26 km), so swap mutation can't escape.
- Fix: inversion mutation (reverse a chunk) - one of Felipe's three mutations. One inversion turns 50.74 into 49.36.
- With inversion (MUTATION_RATE 0.2, half swap / half inversion): stuck at 76.02 min from gen 15-29, ESCAPED at gen 30 -> 73.96 min.
  Best route [3,4,7,8,6,5,2,1,0] = Python [4,5,8,9,7,6,3,2,1] = the true best (49.36 km = 74.04 min in Python). AnyLogic found the optimum.
- One run is one data point. For the thesis: repeat with different seeds and report how often it finds the best.

## Lesson 11 - Dark dashboard (Parts A + B)
- Palette: bg #0F172A, cards #1E293B, grid #334155, text #E2E8F0 / #94A3B8, best = teal #2DD4BF, average = amber #FBBF24, depot = coral #F43F5E.
- Rule: bright colors only for things that mean something (route, chart lines, depot).
- Layout: title bar, map card (left), number tiles + chart + controls cards (right). Canvas 1440 x 820.
- Plot 'fitnessPlot' with auto-update OFF; nextGeneration calls fitnessPlot.updateData() once per generation (x = generation, y = bestFitness / currentAvg).
- Tiles: txtBest/txtGen/txtAvg updated with .setText(String.format("%.1f min", x)).
- Developer elements (parameters, variables, functions) moved to x > 1500, off the dashboard.
- Map: zoom 65000, dark gray Esri tiles (custom tile URL).
- Model uses a FIXED random seed (Simulation experiment -> Randomness), so every run gives the same result.

## Lesson 11 - Part C: best route on the map + modern icons
- drawBestRoute(): runs only when a NEW best route is found. Hides the old shape, builds corner points (depot + stops in route order), draws a closed GISRegion with transparent fill and a 4px teal outline. "Closed" = includes the trip back to Albrook.
- Icons: trucks = small amber dots (population, same color as the average line), stops = white dots, depot = coral dot. The 3D truck model was drawn ~1 km long on the map.
- Dashboard height 796 to fit a laptop screen; Simulation -> Window -> "Maximized size" opens it full screen.

## Lesson 11 - Part D: controls
- Sliders linked to parameters: sliderPop -> POP_SIZE (10-100), sliderGen -> GENERATIONS (20-500), sliderMut -> MUTATION_RATE (0-50%). Value labels use dynamic text (TextCode).
- The GA no longer starts on startup. "Run optimization" button (runButton, OnClick) calls startOptimization(): locks sliders, grays the button, creates POP_SIZE trucks, startGeneration().
- 'started' (boolean) prevents starting twice; button text = started ? "Running..." : "Run optimization".

## Lesson 11 - Stop labels
- Each Stop has a variable visitOrder; drawBestRoute() sets st.visitOrder = i + 1 for the current best route.
- Label next to each dot (dynamic text): (visitOrder > 0 ? visitOrder + "  " : "") + stopName. Depot labelled "Albrook (depot)".
- Button text: "Run optimization" -> "Running..." -> "Done".
- Routing back to straight lines (real roads skipped for now).
- Shorter stop names (Casco Viejo, Pedregal, Tocumen Airport, Rommel Fernández, Costa del Este) + accents; depot label moved to the left of its dot so labels don't overlap.
