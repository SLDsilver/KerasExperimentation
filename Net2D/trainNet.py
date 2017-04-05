#!/usr/bin/env python
import keras
import imp
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras.utils import np_utils

from keras import backend as K

import sys
import imp
import numpy as np
import correct_Complex as c
import load_data_2d as ld
import Net_2 as net



#GLobal variables
itrain = np.zeros((1,0))
otrain = np.zeros((1,0))
itest = np.zeros((1,0))
otest = np.zeros((1,0))

def loadData(train_directory,test_directory):

    num_files = 200
    num_tests = 75
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
    return in_train, out_train, in_test, out_test

if __name__ == "__main__":
    while True:
        configFile = None
        if not (itrain.size and otrain.size and itest.size and otest.size):
            itrain, otrain, itest, otest = loadData('samples','samples2')
        print('Please enter to train Net_2.py (0 to exit): ')
        if(sys.stdin.readline() == '0'):
            exit()
        net = imp.reload(net)
        net.train(itrain,otrain,itest,otest)
