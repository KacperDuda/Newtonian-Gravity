import json
import numpy as np

import os

import datetime
time = datetime.datetime.now().strftime("%m.%d.%H.%M")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # 0 - all messages, 1 - no INFO, 2 - no warning, 3 - no error reporting

import tensorrt
import tensorflow as tf

# adding aliases
Sequential = tf.keras.models.Sequential
Dense = tf.keras.layers.Dense
Dropout = tf.keras.layers.Dropout
BatchNormalization = tf.keras.layers.BatchNormalization
load = tf.keras.models.load_model


def newSection():
    print("===============================")


newSection()
print("Number of GPUs to use: ", len(tf.config.experimental.list_physical_devices('GPU')))

# impoerting data
with open("../data/experiment_one/10k80ms2s.json") as trainingSet:
    data_train = json.load(trainingSet)
    X_train = np.array(data_train["X"])
    Y_train = np.array(data_train["y"])

with open("../data/experiment_one/3p1000i80f25.0d.json") as validatingSet:
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
saved_model = input("Podaj nazwę modelu (brak): ")
if saved_model:
    model = load(f'../model_data/{saved_model}.h5')
    print("Model loaded successfully from file")
else:
    model = Sequential()
    # input layer
    model.add(Dense(16, input_shape=(16,), activation="linear"))


    model.add(Dense(500, activation="relu"))
    model.add(Dropout(0.25))
    model.add(BatchNormalization())

    model.add(Dense(500, activation="relu"))
    model.add(Dropout(0.35))
    model.add(BatchNormalization())

    model.add(Dense(500, activation="relu"))
    model.add(Dropout(0.25))
    model.add(BatchNormalization())

    model.add(Dense(750, activation="relu"))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())

    model.add(Dense(480, activation="linear"))

    model.summary()
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss="mean_squared_error")
newSection()

# TRAINING
for i in range(int(input("Ilość epok * 1000: "))):
    model.fit(X_train, Y_train, epochs=1000, batch_size=1000, validation_data=(X_val, Y_val))
    model.save(f"{os.path.dirname(os.path.dirname(__file__))}/model_data/{time}/{i}.h5")
