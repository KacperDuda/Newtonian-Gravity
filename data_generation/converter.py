import json
from planet import Planet, Position

filenameIn = 'proportionalGravity'
filenameOut = filenameIn + 'Converted'


def get_iterations(data):
    planet_amount = data["planet_amount"]
    iterations_amount = data["iterations"]
    output_frames = data["output_frames_amount"]

    iterations = []
    for i in range(iterations_amount):
        iterations.append({
            "amount": planet_amount,
            "frames": output_frames + 2,  # two input frames are always
            "delta": data["X"][i][0],
            "planets": []
        })

        for j in range(planet_amount):
            planet = Planet(data["X"][i][1 + j], init_first_position=False)

            for k in [0, 1]:  # get two frames for each planet
                planet.positions.append(Position(
                    data["X"][i][1 + planet_amount + 2 * j + 2 * planet_amount * k],
                    data["X"][i][2 + planet_amount + 2 * j + 2 * planet_amount * k]
                ))

            for k in range(output_frames):
                planet.positions.append(Position(
                    data["y"][i][0 + 2 * j + 2 * planet_amount * k],
                    data["y"][i][1 + 2 * j + 2 * planet_amount * k]
                ))

            iterations[i]["planets"].append(planet.toDict())

    return {
        "iterations_amount": iterations_amount,
        "iterations": iterations
    }


def complex_to_simple_from_file(file_in, fileOut):
    with open(f"../data/{file_in}.json") as f_in:
        data = json.load(f_in)

    iterations = get_iterations(data)

    with open(f"../data/{fileOut}.json", "w") as f_out:
        json.dump(iterations, f_out)


if __name__ == "__main__":
    complex_to_simple_from_file(filenameIn, filenameOut)
