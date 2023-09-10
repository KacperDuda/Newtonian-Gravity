from planet import *
from simulator import next_frame
import json
import numpy as np
from main import computational_delta, round_to

# mathematically returning value that will make weighted average to be equal zero
def calc_last_value(masses, coords):
    coord_center = 0
    for idx, coord in enumerate(coords):
        coord_center += coord * masses[idx]

    return -coord_center / masses[-1]


def gen_coordinates_and_velocities(planet_amount):
    masses = np.random.normal(0.5, 0.2, planet_amount)  # all masses have standard distribution
    for idx, mass in enumerate(masses):
        if mass < 0:
            masses[idx] *= -1

    # initial coordinates and velocities will be generated for
    # (planet_amount - 1) planets and one will be calculated in a way that all theoretical assumptions will be fulfilled

    initial_planet_kinetic_values = {
        "coord_x": np.random.normal(0, 0.5, planet_amount - 1).tolist(),
        "coord_y": np.random.normal(0, 0.5, planet_amount - 1).tolist(),
        "velocity_x": np.random.normal(0, 0.2, planet_amount - 1).tolist(),
        "velocity_y": np.random.normal(0, 0.2, planet_amount - 1).tolist()
    }

    for key, value in initial_planet_kinetic_values.items():
        initial_planet_kinetic_values[key].append(calc_last_value(masses, value))

    initial_planet_kinetic_values["masses"] = masses.tolist()

    return initial_planet_kinetic_values


def gen_planets(planet_amount):
    assert planet_amount > 1, "amount of planets must be grater than one"

    # generating until all data is ok
    while True:
        is_ok = True
        planet_kinetic_info = gen_coordinates_and_velocities(planet_amount)

        for key, value in planet_kinetic_info.items():
            if key == 'masses':
                continue
            if abs(value[-1]) > 1:
                is_ok = False

        if is_ok:
            break

    planets = []
    for i in range(planet_amount):
        planets.append(Planet(
            planet_kinetic_info["masses"][i],
            planet_kinetic_info["coord_x"][i],
            planet_kinetic_info["coord_y"][i],
            planet_kinetic_info["velocity_x"][i],
            planet_kinetic_info["velocity_y"][i]
        ))

    return planets


def gen_iteration(planet_amount, output_frames, delta):
    planets = gen_planets(planet_amount)

    for i in range(int((output_frames+1) * delta / computational_delta)):
        next_frame(planets, computational_delta)

    # check for anomalies and start process over if so
    X = []
    Y = []

    X.append(delta) # adding time to the model
    # adding masses of planets - order of neurons does not matter
    for planet in planets:
        X.append(round(planet.m, round_to))

    for i in range(int((output_frames+1) * delta / computational_delta)+1):
        if i % int(delta / computational_delta) == 0:
            frame = []
            for planet in planets:
                frame.append(round(planet.positions[i].x, round_to))
                frame.append(round(planet.positions[i].y, round_to))

            if int(i/int(delta / computational_delta)) < 2:
                X += frame
            else:
                Y += frame


    return X, Y

# generating a give amount of iteration for machine learning and saves it inside files
def generate(planet_amount: int, iterations: int, output_frames: int, delta, filename: str) -> None:
    print("Generating")
    data = {
        "planet_amount": planet_amount,
        "iterations": iterations,
        "output_frames_amount": output_frames,
        "X": [],
        "y": []
    }

    for i in range(iterations):
        (to_X, to_y) = gen_iteration(planet_amount, output_frames, delta)
        data["X"].append(to_X)
        data["y"].append(to_y)
        print(f"{i + 1}/{iterations}, {100 * (i + 1) / iterations:.1f}%")  # adding info about each iteration

    with open(f'../data/{filename}.json', 'w') as output:
        json.dump(data, output)


if __name__ == '__main__':
    p_amount = int(input("Planet Amount: ") or 3)
    iter = int(input("Iterations: ") or 15)
    frames = int(input("Output frames per iteration: ") or 20)
    delta = int(input("Time (in ms) between all frames: ") or 100)
    delta /= 1000
    filename = input("filename: ") or 'test'

    generate(p_amount, iter, frames, delta, filename)
    # generate(2, 1, 300, 0.1, 'best')
