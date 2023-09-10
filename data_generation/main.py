from planet import *
from typing import List
import simulator
import math
import matplotlib.pyplot as plt
import json
import converter

G = 6.31654418845696  # gravity constant in our model
computational_delta = 0.00001  # amount of time between frames in seconds
timeToSimulate = 50  # in seconds
show_delta = 0.01  # showing how often user should have data
round_to = 5

to_plot = True
filename = "tests"


def main():
    # planets: List[Planet] = [
    #     Planet(1, 1, 0, 0, 0.4 * math.pi),
    #     Planet(1, -1, 0, 0, -0.4 * math.pi)
    # ]

    # planets: List[Planet] = [
    #     Planet(1, 1, 1, 0, 0),
    #     Planet(1, -1, 0, 0, 0),
    #     Planet(1, 1.5, -0.5, 0, 0)
    # ]

    planets: List[Planet] = [
        Planet(1, 1, 1, 0, 0),
        Planet(1, -1, 0, 0, 0),
        Planet(3, 0, 0, 0, 0),
        Planet(1, 1.5, -0.5, 0, 0)
    ]

    # simulating
    for i in range(int(timeToSimulate / computational_delta)):
        simulator.next_frame(planets, computational_delta)

    # plotting
    if to_plot:
        for planet in planets:
            x = []
            y = []
            for idx, pos in enumerate(planet.positions):
                if idx % int(show_delta / computational_delta) == 0:
                    x.append(pos.x)
                    y.append(pos.y)
            plt.scatter(x, y, s=1)

        plt.axis('square')
        plt.show()

    else:
        output = {
            "amount": len(planets),
            "frames": 0,
            "delta": show_delta,
            "planets": []
        }

        frame_o_meter = 0

        # saving to a file
        for planet in planets:
            shown_positions = []
            for idx, pos in enumerate(planet.positions):
                if idx % int(show_delta / computational_delta) == 0:
                    shown_positions.append({
                        "x": pos.x,
                        "y": pos.y
                    })
                    frame_o_meter += 1

            output["planets"].append({
                "mass": planet.m,
                "positions": shown_positions
            })

        output["frames"] = frame_o_meter

        with open(f"../data/{filename}.json", "w") as outfile:
            json.dump(output, outfile)


if __name__ == '__main__':
    main()
