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
train_x, train_y = ld.loadDataAlpha(train_directory, 1000, 20000, 100)
train_x = np.array(train_x).reshape(200000, 100, 1)
train_y = np.array(train_y).reshape(200000, 1)
train_y = np_utils.to_categorical(train_y)

#Load the validation tuple
test_x, test_y = ld.loadDataAlpha(test_directory, 20, 20000, 100)
test_x = np.array(test_x).reshape(4000, 100, 1)
test_y = np.array(test_y).reshape(4000, 1)
test_y = np_utils.to_categorical(test_y)
num_signals = test_y.shape[1]


################################# Model Construction ############################

#Adjust model parameters here

#Create the model
model = Sequential()
#Input shape of form: (depth, width, height); For 1D, (width,height)
model.add(Conv1D(64, 3, activation='relu', input_shape=(100, 1)))
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Dropout(.2))
model.add(Conv1D(25, 4, activation='relu'))
model.add(Conv1D(25, 4, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(.2))
model.add(Dense(num_signals,activation='softmax'))

#Compile model
epoches = 10
lrate = .01
decay = lrate / epoches
sgd = SGD(lr = lrate, momentum=.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print(model.summary())

model.fit(train_x, train_y, epochs=epoches, batch_size = 32)
model.save(model_file)
scores = model.evaluate(test_x, test_y, verbose=0)
print("Accuracy: %.2f%%" %(scores[1]*100))
