import json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # 0 - all messages, 1 - no INFO, 2 - no warning, 3 - no error reporting

import tensorrt
import tensorflow as tf

print("Number of GPUs to use: ", len(tf.config.experimental.list_physical_devices('GPU')))

# # impoerting data
# with open("../data/3.0k_madness.json") as trainingSet:
#     data_train = json.load(trainingSet)
#     X = data_train["X"]
#     Y = data_train["y"]
#     print("Data loaded successfully")
#
# with tf.device():
#     model = Sequential()
#
#     model.add(Dense(32, input_dim=13, activation='relu'))
#     # model.add(BatchNormalization())
#
#     model.add(Dense(32, activation='relu'))
#     # model.add(BatchNormalization())
#     model.add(Dropout(0.1))
#
#     model.add(Dense(16, activation='relu'))
#     # model.add(BatchNormalization())
#     model.add(Dropout(0.1))
#
#     model.summary()