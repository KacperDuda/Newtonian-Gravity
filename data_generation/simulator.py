from planet import Planet
from main import G
from typing import List
import math


def radius_squared(planet1: Planet, planet2: Planet, frame: int = -1) -> float:
    return (
            ((planet1.positions[frame].x - planet2.positions[frame].x) ** 2) +
            ((planet1.positions[frame].y - planet2.positions[frame].y) ** 2)
    )


def force_value(planet1: Planet, planet2: Planet):
    return G * planet1.m * planet2.m / radius_squared(planet1, planet2)


def d_y(planet1: Planet, planet2: Planet, frame=-1):
    return planet2.positions[frame].y - planet1.positions[frame].y


def d_x(planet1: Planet, planet2: Planet, frame=-1):
    return planet2.positions[frame].x - planet1.positions[frame].x


def calculate_resultant_force(planets: List[Planet]):
    # loops are arranged in a way that each connection is used once to calculate force change
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            f_val = force_value(planets[i], planets[j])  # force value
            dy = d_y(planets[i], planets[j])  # y diff
            dx = d_x(planets[i], planets[j])  # x diff
            r = math.sqrt(radius_squared(planets[i], planets[j]))  # radius

            # adding to the resultant force of planets
            planets[i].Fwx += f_val * dx / r
            planets[i].Fwy += f_val * dy / r

            # force has sae value but opposite direction so changing a sign
            planets[j].Fwx += - f_val * dx / r
            planets[j].Fwy += - f_val * dy / r


def next_frame(planets: List[Planet], delta):
    calculate_resultant_force(planets)

    for planet in planets:
        planet.next(delta)
