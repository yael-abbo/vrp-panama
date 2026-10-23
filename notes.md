# Lesson notes

## Lesson 1 - The problem
- One truck, a depot in Albrook, 9 stops. Visit each once, come back. Shortest total distance wins.
- One truck = Traveling Salesman Problem. Several trucks = Vehicle Routing Problem.
- Trying every order doesn't scale: 9 stops = 362,880 routes, 20 stops = ~2.4 quintillion.
- A GA "breeds" good routes instead: random routes -> keep the short ones -> combine them -> small random changes -> repeat.
- Distances are straight-line (haversine) for now. Real road distances come later.
- Question for next time: how would you write one route as a Python list?
