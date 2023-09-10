from planet import *
from simulator import next_frame
import json


# generating a give amount of iteration for machine learning and saves it inside files
def generate(planet_amount: int, iterations: int, output_frames: int, delta, filename: str) -> None:
    results = []
    for i in range(iterations):
        print(i)





if __name__ == '__main__':
    p_amount =  int(input("Planet Amount: ") or 3)
    iter = int(input("Iterations: ") or 15)
    frames = int(input("Output rrames per iteration") or 20)
    delta = int(input("Time in ms between all frames") or 100)
    filename = input("filename") or 'test'

    generate(p_amount, iter, frames, delta, filename)


