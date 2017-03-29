from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.optimizers import SGD

import numpy as np
import load_data as ld

train_directory = "samples"
test_directory = 'valid'
model_file = 'model_5C.h5'


#Load the training tuple
train_x, train_y = ld.loadData(train_directory, 1000, 10000)
train_x = np.array(train_x).reshape(1000, 20000, 1)
train_y = np.array(train_y).reshape(1000, 1)
train_y = np_utils.to_categorical(train_y)

#Load the validation tuple
test_x, test_y = ld.loadData(test_directory, 20, 10000)
test_x = np.array(test_x).reshape(20, 20000, 1)
test_y = np.array(test_y).reshape(20, 1)
test_y = np_utils.to_categorical(test_y)
num_signals = test_y.shape[1]


################################# Model Construction ############################

#Adjust model parameters here

#Create the model
model = Sequential()
model.add(Conv1D(64, 5, activation='relu', input_shape=(20000, 1)))
model.add(Dropout(.5))
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Dropout(.5))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Dropout(.5))
model.add(Conv1D(5, 1, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(num_signals,activation='softmax'))

#Compile model
epoches = 25
lrate = .01
decay = lrate / epoches
sgd = SGD(lr = lrate, momentum=.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

print(model.summary())

model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=epoches, batch_size = 32)
model.save(model_file)
scores = model.evaluate(test_x, test_y, verbose=0)
print("Accuracy: %.2f%%" %(scores[1]*100))
