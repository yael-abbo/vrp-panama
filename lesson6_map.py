"""
Lesson 6: Drawing the route on a real map of Panama City.

Uses folium, which builds an interactive web map (Esri street map tiles) and
saves it as an .html file you open in your browser.

Install once:   pip install folium
"""
import folium

from lesson1_setup import stops
from lesson2_chromosome import random_route, route_length, names
from lesson5_full_ga import genetic_algorithm


def route_points(route):
    """Turn a route [3, 1, 7, ...] into map coordinates, depot at both ends."""
    full = [0] + route + [0]
    return [stops[names[i]] for i in full]


def draw_map(best, random_one, filename="lesson6_map.html"):
    # 1. A map centred on Panama City
    m = folium.Map(location=[9.01, -79.48], zoom_start=12, tiles="Esri.WorldStreetMap")   # OSM tiles are blocked when the map is opened as a local file

    # 2. Pins: the depot in red, each stop numbered in its visiting order
    depot = names[0]
    folium.Marker(stops[depot], tooltip="Depot: " + depot,
                  icon=folium.Icon(color="red", icon="home")).add_to(m)
    for order, i in enumerate(best, start=1):
        folium.Marker(
            stops[names[i]],
            tooltip=f"{order}. {names[i]}",
            icon=folium.DivIcon(html=f"""
                <div style="background:#1f6feb;color:white;border-radius:50%;
                            width:24px;height:24px;text-align:center;line-height:24px;
                            font-weight:bold;font-size:13px;border:2px solid white;">
                    {order}</div>"""),
        ).add_to(m)

    # 3. Lines: the GA's best route, and a random route to compare
    best_layer = folium.FeatureGroup(name=f"GA best route ({route_length(best):.1f} km)")
    folium.PolyLine(route_points(best), color="#1f6feb", weight=5, opacity=0.9).add_to(best_layer)
    best_layer.add_to(m)

    rand_layer = folium.FeatureGroup(name=f"A random route ({route_length(random_one):.1f} km)",
                                     show=False)
    folium.PolyLine(route_points(random_one), color="gray", weight=3,
                    dash_array="6", opacity=0.8).add_to(rand_layer)
    rand_layer.add_to(m)

    # 4. A switch in the corner to turn each route on and off
    folium.LayerControl(collapsed=False).add_to(m)

    m.save(filename)
    return filename


if __name__ == "__main__":
    best, _ = genetic_algorithm(verbose=False)
    random_one = random_route()
    print(f"GA best route: {route_length(best):.1f} km")
    print(f"Random route:  {route_length(random_one):.1f} km")
    print("Saved map:", draw_map(best, random_one))
    print("Open it with:  open lesson6_map.html")
