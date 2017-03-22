from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution1D
from keras.utils import np_utils

import numpy as np
import correct_Complex as c

input_train = np.empty([100,10000,2],dtype = complex)
for i in range(0,100):
    inputfile = "samples/samples" + str(i) + ".txt"

    #Imports the data
    c.correct_Complex(inputfile, "data")
    newData = np.loadtxt("data", dtype=complex)

    input_train[i] = np.loadtxt("data", dtype=complex)



#input_test = np.utils.to_categorical(np.loaddata(inputtestfile))

inputtestfile = "samples2/samples0.txt"
outputtestfile = "samples2/modScheme.txt"

outputfile = "samples/modScheme.txt"
output_train = np.loadtxt(outputfile)
output_test = np_utils.to_categorical(np.loadtxt(outputtestfile))
num_classes = output_test.shape[1]


#Create the model
model = Sequential()
model.add(Convolution1D(9000, 1, 1000, input_shape=(5,10000,1), activation = 'relu'))
model.add(Convolution1D(900, 1, 100, activation = 'relu'))
model.add(Convolution1D(90, 1, 10, activation = 'relu'))
model.add(Flatten())
model.add(Dense(num_classes, activation = 'softmax'))

#Compile model
epochs = 25
lrate = .01
decay = lrate/ epochs
sgd = SGD(lr=lrate, momentum = .9, decray = decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

print(model.summary())
