from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.optimizers import SGD
from contextlib import redirect_stdout

import tensorflow as tf
import numpy as np
import load_data as ld

train_directory = "samples2"
test_directory = 'valid'


# Model - Binary Decision Making
# Idea: Train 5 separate networks to see if overall accuracy can be improved.
# Create the First Signal Model
def createModels(num_signals):
    dict_networks = {}
    for i in range(0,num_signals):
        #Binarizes the data
        #Import the data
        train_x, train_y = ld.loadDataBinary(train_directory, 100, 20000, 200,i)
        #Load the validation tuple
        test_x, test_y = ld.loadDataBinary(test_directory, 20, 20000, 200, i)
        num_signals = test_y.shape[1]

        #Model Construction
        model_ID = "model" + str(i)
        model = Sequential()
        # Input shape of form: (depth, width, height); For 1D, (width,height)
        model.add(Conv1D(2, 100, activation='relu', input_shape=(200, 1)))
        model.add(Dropout(.2))
        model.add(Conv1D(12, 64, activation='relu'))
        # model.add(MaxPooling1D(2))
        model.add(Dropout(.2))
        model.add(GlobalAveragePooling1D())
        model.add(Dropout(.2))
        model.add(Dense(256, activation='relu'))
        layer_final = Dense(num_signals, activation='softmax')
        model.add(layer_final)

        # Compile model
        epoches = 10
        lrate = .01
        decay = lrate / epoches
        sgd = SGD(lr=lrate, momentum=.9, decay=decay, nesterov=False)
        model.compile(loss='binary_crossentropy',
                              optimizer=sgd,
                              metrics=['accuracy'])

        #print(model.summary())

        # Model training
        model.fit(train_x, train_y, epochs=epoches, batch_size=32, validation_data=(test_x, test_y))

        #Add to dictionary
        #dict_networks[modelID] = model

        #Results
        scores = model.evaluate(test_x, test_y, verbose=0)
        location = "brute_binaryexploration/exploration" + str(i) + ".txt"
        with open(location, 'a+') as f:
            f.write("The actual solutions are below.")
            f.write("\n")
            f.write(np.array_str(test_y))
            f.write("\n")
            f.write("The model predicted that ... ")
            f.write("\n")
            sess = tf.InteractiveSession()
            a = tf.constant(layer_final.output)
            tf.Print(a, 
            f.write("\n")
            f.write("Accuracy: %.2f%%" % (scores[1] * 100))
createModels(5)
