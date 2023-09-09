from planet import *
from typing import List
import simulator
import matplotlib.pyplot as plt
import json

G = 6.31654418845696  # gravity constant in our model
computational_delta = 0.000001  # amount of time between frames in seconds
timeToSimulate = 10  # in seconds
show_delta = 0.1


def main():
    planets: List[Planet] = [
        Planet(1, 1, 0, 0, 1.26),
        Planet(1, -1, 0, 0, -1.26),
        # Planet(3, 3, 3, 0, 0)
    ]

    # simulating
    for i in range(int(timeToSimulate / computational_delta)):
        simulator.next_frame(planets, computational_delta)

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

    output = {
        "amount": len(planets),
        "delta": show_delta,
        "planets": []
    }

    for planet in planets:
        shown_positions = []
        for idx, pos in enumerate(planet.positions):
            if idx % int(show_delta / computational_delta) == 0:
                shown_positions.append({
                    "x": pos.x,
                    "y": pos.y
                })

        output["planets"].append({
            "mass": planet.m,
            "positions": shown_positions
        })

    with open("../data/sample.json", "w") as outfile:
        json.dump(output, outfile)


if __name__ == '__main__':
    main()
