"""
Lesson 1: Setting up the problem.

One truck starts at a depot in Albrook, visits every stop once,
and comes back. Here we just write down where the places are and
measure distances between them.
"""
import math

# Each place and its location (latitude, longitude).
# The first one is the depot: where the truck starts and ends.
# Coordinates are approximate - check them on Google Maps.
stops = {
    "Depot - Albrook":  (8.973, -79.551),
    "Casco Viejo":      (8.952, -79.535),
    "Obarrio":          (8.990, -79.520),
    "Bethania":         (9.005, -79.525),
    "Pueblo Nuevo":     (9.010, -79.500),
    "San Miguelito":    (9.033, -79.500),
    "Costa del Este":   (9.010, -79.465),
    "Juan Diaz":        (9.035, -79.450),
    "Pedregal":         (9.060, -79.430),
    "Tocumen":          (9.080, -79.380),
}


def distance_km(a, b):
    """Straight-line distance between two points on Earth, in km (haversine)."""
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))  # 6371 = Earth's radius in km


if __name__ == "__main__":
    names = list(stops)
    print(f"{len(names) - 1} stops plus the depot\n")
    for n in names[1:]:
        print(f"Albrook -> {n:15s} {distance_km(stops[names[0]], stops[n]):5.1f} km")
    print("\nPossible routes:", math.factorial(len(names) - 1))
