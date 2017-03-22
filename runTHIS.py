from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution1D

import numpy as np
import correct_Complex as c


from pymatbridge import Matlab

inputfile = ""
outputfile = ""
inputtestfile = ""
outputtestfile = ""

#Imports the data
input_train = np.loaddata(inputfile)
output_train = np.loaddata(outputfile)
input_test = np.utils.to_categorical(np.loaddata(inputtestfile))
output_test = np.utils.to_categorical(np.loaddata(outputtestfile))
num_classes = output_test.shape[1]


#Create the model
model = Sequential()
model.add(Convolution1D(9000, 1, 1000, input_shape=(5,1,10000), activation = 'relu')
model.add(Convolution1D(900, 1, activation = 'relu')
model.add(Convolution1D(90, 1, activation = 'relu')
model.add(Flatten())
model.add(Dense(num_classes, activation = 'softmax'))

#Compile model
epochs = 25
lrate = .01
decay = lrate/ epochs
sgd = SGD(lr=lrate, momentum = .9, decray = decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

print(model.summary())
    
