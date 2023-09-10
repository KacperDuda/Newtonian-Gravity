import json

filename = 'pythonRealTest'


def complex_to_simple_from_file(file):
    with open(f"../data/{file}.json") as f:
        data = json.load(f)

    planet_amount = data["planet_amount"]
    iterations = data["iterations"]
    output_frames = data["output_frames_amount"]

    planet_sets = []
    for i in range(iterations):
        print(i)

if __name__ == "__main__":
    complex_to_simple_from_file(filename)