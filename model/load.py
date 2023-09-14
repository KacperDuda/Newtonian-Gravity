import json
import numpy as np

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # 0 - all messages, 1 - no INFO, 2 - no warning, 3 - no error reporting

import tensorrt
import tensorflow as tf

# adding aliases
Sequential = tf.keras.models.Sequential
Dense = tf.keras.layers.Dense
Dropout = tf.keras.layers.Dropout
BatchNormalization = tf.keras.layers.BatchNormalization

load = tf.keras.models.load_model


filename = "experiment_one/3p1000i80f25.0d"

with open(f"../data/{filename}.json") as f:
    data = json.load(f)

X = np.array(data["X"])
Y_numerical = np.array(data["y"])

model = load('../model_data/09.13.20.11/19.h5')
Y_predicted = model.predict(X)

X_final = []
for x in X:
    X_final.append(x.tolist())
    X_final.append(x.tolist())

Y_final = []
for i in range(len(Y_numerical)):
    Y_final.append(Y_numerical[i].tolist())
    Y_final.append(Y_predicted[i].tolist())

result = {
    "planet_amount": int((len(X[0]) - 1) / 5),
    "iterations": 2*int(len(X)),
    "output_frames_amount": data["output_frames_amount"],
    "X": X_final,
    "y": Y_final
}


with open(f"../data/predicted/{filename}.json", "w") as file:
    json.dump(result, file)
