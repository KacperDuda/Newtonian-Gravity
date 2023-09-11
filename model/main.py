
import tensorflow
from tensorflow.keras.models import Sequential # no feedback loop
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization

# nothing is ready
# print("Num GPUs Available: ", len(tensorflow.config.experimental.list_physical_devices('GPU'))


model = Sequential()

model.add(Dense(32, input_dim=13, activation='relu'))
# model.add(BatchNormalization())

model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
model.add(Dropout(0.1))

model.add(Dense(16, activation='relu'))
# model.add(BatchNormalization())
model.add(Dropout(0.1))

model.summary()