from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D

import numpy as np
import load_data as ld

train_directory = "samples"
test_directory = 'not yet defined'


#Load the training tuple
train_x, train_y = ld.loadData(train_directory, 10, 10000)
train_x = np.array(train_x).reshape(10, 20000, 1)
train_y = np.array(train_y).reshape(10, 1)

train_y = np_utils.to_categorical(train_y)
num_signals = train_y.shape[1]
print(num_signals)



################################# Model Construction ############################

#Adjust model parameters here

#Create the model
model = Sequential()
#Input volume is a 
layer = Conv1D(64, 5, activation='relu', input_shape=(20000, 1))
model.add(layer)
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Conv1D(128, 3, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(.5))
model.add(Dense(num_signals,activation='sigmoid'))

#Compile model
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print(model.summary())

model.fit(train_x, train_y, batch_size = 16, epochs=20)

