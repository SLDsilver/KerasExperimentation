import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras.utils import np_utils

from keras import backend as K

import numpy as np
import correct_Complex as c
import load_data_2d as ld

# input_train = np.empty([20000, 100, 1],dtype = float)
#
# #Load the input data
# newData = np.loadtxt("dataNoI", dtype=float)
# input_train = newData.reshape([20000, 100, 1])
# print('Input volume is:' + str(input_train.shape))
#
# #Load the correct answer
# outputfile = "modScheme.txt"
# #Adjust OutputFile
# c.adjust_Output("samples/modScheme.txt", outputfile, 200)
# output_train = np.loadtxt(outputfile)
# print('Output volume is: ' + str(output_train.shape))
#
# #Load the testing data
# inputtestfile = "samples2/samples0.txt"
# outputtestfile = "samples2/modScheme.txt"
#
# output_test = np_utils.to_categorical(np.loadtxt(outputtestfile))
# num_classes = output_test.shape[1]
# print('Num_classes is' + str(num_classes))

train_directory = "samples"
test_directory = 'not yet defined'

num_files = 1
num_samples = 10000


#Load the training tuple
train_x, train_y = ld.loadData(train_directory, num_files, num_samples)
# train_x = np.array(train_x).reshape(num_files, num_samples, 2)
# train_y = np.array(train_y).reshape(num_files, 1)

train_y = np_utils.to_categorical(train_y)
num_signals = train_y.shape[1]

################################# Model Construction ############################
#Adjust model parameters here
input_shape = (100, 2, 1) #10k sample points, real and complex, one point deep

#Create Net Structure
model = Sequential()

#First block
#2d Convolutional net 10000 input values
model.add(Conv2D(10,(2, 2),padding='same',input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,1)))
model.add(Dropout(0.25))

model.add(Conv2D(20,(2,2),padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,1)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(100))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(5))
model.add(Activation('softmax'))

print(model.summary())
model.fit(input_train, output_train, batch_size = 10, epochs=10)
#print(model.evaluate(input_test, output_test, batch_size=1))
