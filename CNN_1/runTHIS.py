from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D

import numpy as np
import correct_Complex as c

input_train = np.empty([20000, 100, 1],dtype = float)

'''
for i in range(0, 100):
    inputfile = "samples/samples" + str(i) + ".txt"
    c.correct_Complex(inputfile, "data")
    c.remove_Imaginary("data", "dataNoI")
    newData = np.loadtxt("dataNoI", dtype=float)
    print("Currently processing: " + inputfile)
'''

#Load the input data
newData = np.loadtxt("dataNoI", dtype=float)
input_train = newData.reshape([20000, 100, 1])
print('Input volume is:' + str(input_train.shape))

#Load the correct answer
outputfile = "modScheme.txt"
#Adjust OutputFile
c.adjust_Output("samples/modScheme.txt", outputfile, 200)
output_train = np.loadtxt(outputfile)
print('Output volume is: ' + str(output_train.shape))

#Load the testing data
inputtestfile = "samples2/samples0.txt"
outputtestfile = "samples2/modScheme.txt"

output_test = np_utils.to_categorical(np.loadtxt(outputtestfile))
num_classes = output_test.shape[1]
print('Num_classes is' + str(num_classes))


################################# Model Construction ############################

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
