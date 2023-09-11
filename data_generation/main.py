from planet import *
from typing import List
import math
import matplotlib.pyplot as plt
import json
import converter
import generator

from constants import *

to_file = True
filename = "nice"


def main():
    planets: List[Planet] = [
        Planet(1, 1, 0, 0, 0.4 * math.pi),
        Planet(1, -1, 0, 0, -0.4 * math.pi)
    ]

    # planets: List[Planet] = [
    #     Planet(1, 1, 1, 0, 0),
    #     Planet(1, -1, 0, 0, 0),
    #     Planet(1, 1.5, -0.5, 0, 0)
    # ]

    # planets: List[Planet] = [
    #     Planet(1, 1, 1, 0, 0),
    #     Planet(1, -1, 0, 0, 0),
    #     Planet(3, 0, 0, 0, 0),
    #     Planet(1, 1.5, -0.5, 0, 0)
    # ]

    # simulating
    x, y = generator.gen_iteration(len(planets), (int(timeToSimulate / show_delta) - 2), show_delta, planets)
    processed_data = {
        "planet_amount": len(planets),
        "iterations": 1,
        "output_frames_amount": int(timeToSimulate / show_delta) - 2,
        "X": [x],
        "y": [y]
    }

    output = converter.get_iterations(processed_data)

    with open(f"../data/{filename}.json", "w") as f:
        json.dump(output, f)

    # plotting
    # for planet in planets:
    #     x = []
    #     y = []
    #     for idx, pos in enumerate(planet.positions):
    #         if idx % int(show_delta / computational_delta) == 0:
    #             x.append(pos.x)
    #             y.append(pos.y)
    #     plt.scatter(x, y, s=1)
    #
    # plt.axis('square')
    # plt.show()


if __name__ == '__main__':
    main()
