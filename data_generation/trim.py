import json
from converter import get_iterations

with open("../data/predicted/experiment_one/3p1000i80f25.0d.json") as file:
    data = json.load(file)

limit = 250

data["iterations"] = 250
data["X"] = data["X"][0:limit]
data["y"] = data["y"][0:limit]

with open("../data/predicted/experiment_one/3p1000i80f25.0d-trimed.json", "w") as out:
    json.dump(get_iterations(data), out)