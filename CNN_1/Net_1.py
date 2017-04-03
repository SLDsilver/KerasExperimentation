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

train_directory = 'samples'
test_directory = 'tests'

num_files = 10
num_tests = 3
num_samples = 10000


#Load the training tuple
print('Loading training data')
in_train, out_train = ld.loadData(train_directory, num_files, num_samples)
in_train = np.array(in_train).reshape(num_files*100, num_samples/100, 2, 1)
out_train = np.array(out_train).reshape(num_files*100, 1)

out_train = np_utils.to_categorical(out_train,5)
#num_signals = train_y.shape[1]

#Load the testing tuple
print('Loading test data')
in_test, out_test = ld.loadData(test_directory,num_tests,num_samples)
in_test = np.array(in_test).reshape(num_tests*100, num_samples/100, 2, 1)
out_test = np.array(out_test).reshape(num_tests*100, 1)

out_test = np_utils.to_categorical(out_test,5)

num_signals = 5;

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
model.add(Dropout(0.1))

model.add(Conv2D(20,(2,2),padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,1)))
model.add(Dropout(0.1))

model.add(Flatten())
model.add(Dense(100))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(5))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print(model.summary())
model.fit(in_train, out_train, batch_size = 10, epochs=25)
model.save('Trained_Net1_0')
print('Evaluation:')
print(model.evaluate(in_test, out_test, batch_size=1))
