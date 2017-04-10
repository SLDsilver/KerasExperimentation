from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.utils import np_utils
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.optimizers import SGD
from contextlib import redirect_stdout

import numpy as np
import load_data as ld

def catergorical_model(size, num_signals, depth):
    #Model Construction
    # Create the model
    model = Sequential()
    #Input shape of form: (depth, width, height); For 1D, (width,height)
    model.add(Conv1D(32, 2, activation='relu', input_shape=(size, depth)))
    model.add(Conv1D(32, 2, activation='relu'))
    model.add(Dropout(.2))
    #model.add(Conv1D(4, 2, activation='relu'))
    #model.add(Conv1D(4, 2, activation='relu'))
    #model.add(Dropout(.2))
    #model.add(Conv1D(2, 2, activation='relu'))
    #model.add(Conv1D(64, 10, activation='relu'))
    #model.add(Conv1D(32, 2, activation='relu'))
    model.add(Dropout(.2))
    model.add(Flatten())
    model.add(Dropout(.2))
    #model.add(Dense(256, activation='relu'))
    #model.add(Dense(512, activation='relu'))
    #model.add(Dense(5096, activation='relu'))
    #model.add(Dense(2048, activation='relu'))
    model.add(Dense(num_signals, activation='softmax'))

    # Compile model
    #epoches = 2
    #lrate = .01
    #decay = lrate / epoches
    #sgd = SGD(lr=lrate, momentum=.9, decay=decay, nesterov=False)
    model.compile(loss='categorical_crossentropy',
                  optimizer= 'adam',
                  metrics=['accuracy'])

    print(model.summary())
    return model

def activate(model, train_x, train_y, test_x, test_y):
    # Model training
    model.fit(train_x, train_y, epochs=2, batch_size=52, validation_data=(test_x, test_y))
    # model.save(model_file)
    scores = model.evaluate(test_x, test_y, verbose=0)

    #Document the results
    location = "brute_exploration/exploration" + ".txt"
    with open(location, 'a+') as f:
        f.write( str(32) + "\t" + str(20))
        f.write("\t%.2f%%" % (scores[1] * 100))
        f.write("\n")

    



