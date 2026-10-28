"""
Lesson 1: Setting up the problem.

One truck starts at a depot in Albrook, visits every stop once,
and comes back. Here we just write down where the places are and
measure distances between them.
"""
import math

# Each stop is a specific landmark, so you can check it on Google Maps.
# The first one is the depot: where the truck starts and ends.
# Format: "Landmark (area)": (latitude, longitude)
stops = {
    "Depot - Albrook Mall (Albrook)":         (8.97435, -79.55264),
    "Plaza de la Independencia (Casco)":      (8.95246, -79.53472),
    "Hospital del Nino (Curundu)":            (8.96877, -79.53215),
    "Parque Urraca (Bella Vista)":            (8.97536, -79.52730),
    "USMA (Bethania / El Dorado)":            (9.02892, -79.52136),
    "Los Andes Mall (San Miguelito)":         (9.05208, -79.50827),
    "Parque Costa del Este (Costa del Este)": (9.01483, -79.48012),
    "Estadio Rommel Fernandez (Juan Diaz)":   (9.03586, -79.46950),
    "Centro de Salud de Pedregal (Pedregal)": (9.07022, -79.42422),
    "Aeropuerto de Tocumen (Tocumen)":        (9.06909, -79.38301),
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
        print(f"Albrook -> {n:40s} {distance_km(stops[names[0]], stops[n]):5.1f} km")
    print("\nPossible routes:", math.factorial(len(names) - 1))
