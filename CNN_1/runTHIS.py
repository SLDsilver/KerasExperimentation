from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.optimizers import SGD
from contextlib import redirect_stdout

import numpy as np
import load_data as ld

train_directory = "samples2"
test_directory = 'valid'
model_file = 'model_2C.h5'

#Data Importation
#Load the training tuple
train_x, train_y = ld.loadDataAlpha(train_directory, 100, 20000, 200)

#Load the validation tuple
test_x, test_y = ld.loadDataAlpha(test_directory, 20, 20000, 200)
num_signals = test_y.shape[1]

#Model Construction
j = 4
for i in range(1,96):
    for j in range(1, 100):
        for k in range(0, 3):
            # Create the model
            model = Sequential()
            # Input shape of form: (depth, width, height); For 1D, (width,height)
            model.add(Conv1D(i, j, activation='relu', input_shape=(200, 1)))
            model.add(Dropout(.2))
            #model.add(Conv1D(i, j, activation='relu'))
            #model.add(MaxPooling1D(2))
            #model.add(Dropout(.2))
            model.add(GlobalAveragePooling1D())
            model.add(Dropout(.2))
            model.add(Dense(256, activation='relu'))
            model.add(Dense(num_signals, activation='softmax'))

            # Compile model
            epoches = 10
            lrate = .01
            decay = lrate / epoches
            sgd = SGD(lr=lrate, momentum=.9, decay=decay, nesterov=False)
            model.compile(loss='categorical_crossentropy',
                          optimizer=sgd,
                          metrics=['accuracy'])

            #print(model.summary())
            # Model training
            model.fit(train_x, train_y, epochs=epoches, batch_size=32, validation_data=(test_x, test_y))
            # model.save(model_file)
            scores = model.evaluate(test_x, test_y, verbose=0)
            #Document the results
            location = "brute_exploration/exploration" + str(i) + str(j) + ".txt"
            with open(location, 'a+') as f:
                f.write("Model uses: " + str(i) + " filters and " + str(j) + " activation area\t")
                f.write("Accuracy: %.2f%%" % (scores[1] * 100))
                f.write("\n")





