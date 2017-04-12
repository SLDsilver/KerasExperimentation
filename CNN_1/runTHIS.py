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
    model.add(Conv1D(64, 2, activation='relu', input_shape=(size, depth), padding='same'))
    model.add(Dropout(.2))
    model.add(Conv1D(64, 2, activation='relu', padding='same'))
    model.add(MaxPooling1D(4))
    model.add(Conv1D(64, 2, activation='relu', padding='same'))
    model.add(Conv1D(64, 2, activation='relu', padding='same'))
    model.add(MaxPooling1D(4))
    model.add(Dropout(.2))
    model.add(Conv1D(64, 2,activation='sigmoid'))
    model.add(MaxPooling1D(4))
    model.add(Flatten())
    model.add(Dropout(.2))
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
    model.fit(train_x, train_y, epochs=10, batch_size=16, validation_data=(test_x, test_y))
    # model.save(model_file)
    scores = model.evaluate(test_x, test_y, verbose=0)

    #Document the results
    location = "brute_exploration/exploration" + ".txt"
    with open(location, 'a+') as f:
        f.write( str(32) + "\t" + str(20))
        f.write("\t%.2f%%" % (scores[1] * 100))
        f.write("\n")

    



