import json
import numpy as np

import os

import datetime
time = datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # 0 - all messages, 1 - no INFO, 2 - no warning, 3 - no error reporting

import tensorrt
import tensorflow as tf

# adding aliases
Sequential = tf.keras.models.Sequential
Dense = tf.keras.layers.Dense
Dropout = tf.keras.layers.Dropout
BatchNormalization = tf.keras.layers.BatchNormalization


def newSection():
    print("===============================")


newSection()
print("Number of GPUs to use: ", len(tf.config.experimental.list_physical_devices('GPU')))

# # impoerting data
with open("../data/10k80ms2s.json") as trainingSet:
    data_train = json.load(trainingSet)
    X_train = np.array(data_train["X"])
    Y_train = np.array(data_train["y"])

with open("../data/2k80ms2s.json") as validatingSet:
    data_train = json.load(validatingSet)
    X_val = np.array(data_train["X"])
    Y_val = np.array(data_train["y"])

newSection()
print("Data loaded")
print("Training data:")
print("    X shape: ", X_train.shape)
print("    Y shape: ", Y_train.shape)
print("Validating data shape:")
print("    X shape: ", X_val.shape)
print("    Y shape: ", Y_val.shape)
newSection()
print(f"Model input is {X_train.shape[1]} neurons and output is {Y_train.shape[1]} neurons")
print(f"Training size: {X_train.shape[0]}, validation size: {Y_train.shape[0]}")

newSection()

model = Sequential()
# input layer
model.add(Dense(16, input_shape=(16,), activation="linear"))

for i in range(5):
    model.add(Dense(500 + (50*i), activation="linear"))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))

model.add(Dense(474, activation="linear"))

model.summary()
model.compile(optimizer="adam", loss="mean_squared_error")
newSection()

# TRAINING
for i in range(100):
    model.fit(X_train, Y_train, epochs=1000, batch_size=1000, validation_data=(X_val, Y_val))
    model.save(f"{os.path.dirname(os.path.dirname(__file__))}/model_data/{time}/{i}.h5")
