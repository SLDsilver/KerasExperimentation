#!/usr/bin/env python
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras.utils import np_utils

from keras import backend as K


def train(in_train,out_train,in_test,out_test,net_name):
    ################################# Model Construction ############################
    #Adjust model parameters here
    input_shape = (100, 2, 1) #10k sample points, real and complex, one point deep

    #Create Net Structure
    model = Sequential()

    #First block
    #2d Convolutional net 10000 input values
    model.add(Conv2D(128,(10, 2),padding='same',input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(5,1)))
    model.add(Dropout(0.5))

    model.add(Conv2D(64,(10,2),padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(500))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adadelta',  metrics=['accuracy'])

    print(model.summary())
    earlyStop = keras.callbacks.EarlyStopping(monitor='val_acc', min_delta = 0.002, patience = 1, verbose = 1, mode = 'auto')

    model.fit(in_train, out_train, batch_size = 11, epochs=20, validation_data=(in_test,out_test), callbacks = [earlyStop])
    model.save(net_name)
    print('Evaluation:')
    print(model.evaluate(in_test, out_test, batch_size=1))


def train2(in_train,out_train,in_test,out_test,net_name):
    ################################# Model Construction ############################
    #Adjust model parameters here
    input_shape = (100, 2, 1) #10k sample points, real and complex, one point deep

    #Create Net Structure
    model = Sequential()

    #First block
    #2d Convolutional net 10000 input values
    model.add(Conv2D(10,(10, 2),padding='same',input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(5,1)))
    model.add(Dropout(0.25))

    model.add(Conv2D(40,(10,2),padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,1)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(400))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='rmsprop',  metrics=['accuracy'])

    #print(model.summary())

    model.fit(in_train, out_train, batch_size = 11, epochs=100, validation_data=(in_test,out_test))
    model.save(net_name)
    print('Evaluation:')
    print(model.evaluate(in_test, out_test, batch_size=1))
#Signal Number |  accuracy
#      0       |     >98
#      1       |      92
#      2       |      80
#      3       |      77
#      4       |      92
