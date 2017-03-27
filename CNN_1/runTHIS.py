from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D

import numpy as np
import load_data as ld

train_directory = "samples"
test_directory = 'not yet defined'

#Load the training tuple
input_x, input_y = ld.loadData(train_directory, 10, 10000)




'''################################# Model Construction ############################

#Adjust model parameters here

#Create the model
model = Sequential()
#Input volume is a 
layer = Conv1D(64, 5, activation='relu', input_shape=(100, 1))
model.add(layer)
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Conv1D(128, 3, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(.5))
model.add(Dense(1,activation='sigmoid'))

#Compile model
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print(model.summary())
print(layer.input)
print(layer.output)
model.fit(input_train, output_train, batch_size = 16, epochs=10)
print(model.evaluate(input_test, output_test, batch_size=1))
'''
