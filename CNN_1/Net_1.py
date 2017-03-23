import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras.utils import np_utils

from keras import backend as K

import numpy as np
import correct_Complex as c

# input_train = np.empty([100,10000,2],dtype = complex)
# for i in range(0,100):
#     inputfile = "samples/samples" + str(i) + ".txt"
#
#     #Imports the data
#     c.correct_Complex(inputfile, "data")
#     newData = np.loadtxt("data", dtype=complex)
#
#     input_train[i] = np.loadtxt("data", dtype=complex)



#input_test = np.utils.to_categorical(np.loaddata(inputtestfile))

# inputtestfile = "samples2/samples0.txt"
# outputtestfile = "samples2/modScheme.txt"
#
# outputfile = "samples/modScheme.txt"
# output_train = np.loadtxt(outputfile)
# output_test = np_utils.to_categorical(np.loadtxt(outputtestfile))
# num_classes = output_test.shape[1]


input_shape = (1000, 2, 1) #10k sample points, real and complex, one point deep
batch_size = 10
pool_factor = 10

#Create Net Structure
model = Sequential()

#First block
#2d Convolutional net 10000 input values
model.add(Conv2D(batch_size,(999, 2),padding='same',input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(pool_factor,1)))
model.add(Dropout(0.25))

model.add(Conv2D(batch_size*pool_factor,(99,2),padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(pool_factor,1)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1000))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(5))
model.add(Activation('softmax'))

print(model.summary())
