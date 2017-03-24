from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D

import numpy as np
import correct_Complex as c

input_train = np.empty([200, 100],dtype = float)

for i in (0, 99):
    inputfile = "samples/samples" + str(i) + ".txt"
    c.correct_Complex(inputfile, "data")
    c.remove_Imaginary("data", "dataNoI")
    newData = np.loadtxt("dataNoI", dtype=float)

newData.reshape([200, 100])

#Load the data
inputtestfile = "samples2/samples0.txt"
outputtestfile = "samples2/modScheme.txt"

outputfile = "samples/modScheme.txt"
output_train = np.loadtxt(outputfile)
output_test = np_utils.to_categorical(np.loadtxt(outputtestfile))
num_classes = output_test.shape[1]


################################# Model Construction ############################

#Adjust model parameters here

#Create the model
model = Sequential()
layer = Conv1D(100, 10, activation='relu', input_dim=10000)
model.add(layer)

#Compile model
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print(model.summary())
print(layer.input)
print(layer.output)
model.fit(input_train, output_train, batch_size = 16)
print(model.evaluate(input_test, output_test, batch_size=16))
