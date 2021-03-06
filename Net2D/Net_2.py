#!/usr/bin/env python
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras.utils import np_utils

from keras import backend as K


def train(in_train,out_train,in_test,out_test,save_name):
    ################################# Model Construction ############################
    #Adjust model parameters here
    input_shape = (10000, 2, 1) #10k sample points, real and complex, one point deep

    #Create Net Structure
    model = Sequential()

    #First block
    #2d Convolutional net 10000 input values
    model.add(Conv2D(64,(10, 2),padding='same',input_shape=input_shape))
    model.add(Activation('sigmoid'))
    model.add(MaxPooling2D(pool_size=(5,1)))
    model.add(Dropout(0.1))

    model.add(Conv2D(64,(10,2),padding='same'))
    model.add(Activation('sigmoid'))
    model.add(MaxPooling2D(pool_size=(2,1)))
    model.add(Dropout(0.00))

    model.add(Conv2D(64,(10,2),padding='same'))
    model.add(Activation('sigmoid'))
    model.add(MaxPooling2D(pool_size=(2,1)))
    model.add(Dropout(0.1))

    model.add(Flatten())
    model.add(Activation('sigmoid'))
    model.add(Dropout(0.25))
    model.add(Dense(5))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print(model.summary())

    model.fit(in_train, out_train, batch_size = 10, epochs=10, validation_data=(in_test,out_test))
    model.save(save_name)
    print('Evaluation:')
    print(model.evaluate(in_test, out_test, batch_size=1))
