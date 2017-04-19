#!/usr/bin/env python
import keras
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
import load_data_2d_10k as ld10k
from random import randint



#GLobal variables
itrain = np.zeros((1,0))
otrain = np.zeros((1,0))
itest = np.zeros((1,0))
otest = np.zeros((1,0))
net_index = 0

def loadData(train_directory,test_directory):

    num_files = 5
    num_tests = 2
    num_samples = 10000

    #Load the training tuple
    print('Loading training data')
    in_train, out_train = ld.loadData(train_directory, num_files, num_samples)
    in_train = np.array(in_train).reshape(num_files*100, num_samples/100, 2, 1)
    out_train = np.array(out_train).reshape(num_files*100, 1)

    out_train = np_utils.to_categorical(out_train,5)
    #num_signals = train_y.shape[1]

    #Loadthe testing tuple
    print('Loading test data')
    in_test, out_test = ld.loadData(test_directory,num_tests,num_samples)
    in_test = np.array(in_test).reshape(num_tests*100, num_samples/100, 2, 1)
    out_test = np.array(out_test).reshape(num_tests*100, 1)

    out_test = np_utils.to_categorical(out_test,5)
    return in_train, out_train, in_test, out_test

def loadData10k(train_directory,test_directory):

    num_files = 5
    num_tests = 5
    num_samples = 10000

    #Load the training tuple
    print('Loading training data')
    in_train, out_train = ld10k.loadData(train_directory, num_files, num_samples)
    in_train = np.array(in_train).reshape(num_files, num_samples, 2, 1)
    out_train = np.array(out_train).reshape(num_files, 1)

    out_train = np_utils.to_categorical(out_train,5)
    #num_signals = train_y.shape[1]

    #Loadthe testing tuple
    print('Loading test data')
    in_test, out_test = ld10k.loadData(test_directory,num_tests,num_samples)
    in_test = np.array(in_test).reshape(num_tests, num_samples, 2, 1)
    out_test = np.array(out_test).reshape(num_tests, 1)

    out_test = np_utils.to_categorical(out_test,5)
    return in_train, out_train, in_test, out_test

def loadDataBinary(train_directory,test_directory):
    num_files = 20  #Number of files per signal, not total
    num_tests = 10   #Number of training files per signal, not total
    num_samples = 10000 #Number of smaples per file
    spf = 100

    #Instantiate empty arrays
    in_train = np.zeros(shape = (5,num_files*100, num_samples/100, 2, 1))
    out_train  = np.zeros(shape = (5,num_files*100,1))
    in_test  = np.zeros(shape = (5,num_tests*100, num_samples/100, 2, 1))
    out_test  = np.zeros(shape = (5,num_tests*100,1))

    in_train_binary = np.zeros(shape = (5,num_files*200, num_samples/100, 2, 1))
    in_test_binary = np.zeros(shape = (5,num_tests*200, num_samples/100, 2, 1))
    out_train_binary = np.zeros(shape = (5,num_files*200,1))
    out_test_binary = np.zeros(shape = (5,num_tests*200,1))

    #Load the training tuple
    print("\nLoading training for signal: 0")
    in_train[0], out_train[0] = ld.loadDataSplit(train_directory + '_0', num_files, num_samples, spf)
    print("\nLoading training for signal: 1")
    in_train[1], out_train[1] = ld.loadDataSplit(train_directory + '_1', num_files, num_samples, spf)
    print("\nLoading training for signal: 2")
    in_train[2], out_train[2] = ld.loadDataSplit(train_directory + '_2', num_files, num_samples, spf)
    print("\nLoading training for signal: 3")
    in_train[3], out_train[3] = ld.loadDataSplit(train_directory + '_3', num_files, num_samples, spf)
    print("\nLoading training for signal: 4")
    in_train[4], out_train[4] = ld.loadDataSplit(train_directory + '_4', num_files, num_samples, spf)

    print("\nLoading testing for signal: 0")
    in_test[0], out_test[0] = ld.loadDataSplit(test_directory + '_0', num_tests, num_samples, spf)
    print("\nLoading testing for signal: 1")
    in_test[1], out_test[1] = ld.loadDataSplit(test_directory + '_1', num_tests, num_samples, spf)
    print("\nLoading testing for signal: 2")
    in_test[2], out_test[2] = ld.loadDataSplit(test_directory + '_2', num_tests, num_samples, spf)
    print("\nLoading testing for signal: 3")
    in_test[3], out_test[3] = ld.loadDataSplit(test_directory + '_3', num_tests, num_samples, spf)
    print("\nLoading testing for signal: 4")
    in_test[4], out_test[4] = ld.loadDataSplit(test_directory + '_4', num_tests, num_samples, spf)

    signal_num = 0
    for signal_num in range(0,5):
        #Training Data
        i = 0
        j = 0
        for i in range(0,num_files*100):
            in_train_binary[signal_num,i] = in_train[signal_num,i]
            out_train_binary[signal_num,i] = 1

        for j in range(num_files*100,num_files*200):
            rand_signal_num = signal_num
            while (rand_signal_num == signal_num):
                rand_signal_num = randint(0,4)

            in_train_binary[signal_num,j] = in_train[rand_signal_num,randint(0,num_files*100-1)]
            out_train_binary[signal_num,j] = (signal_num == rand_signal_num)


        #shuffle around data
        rng_state = np.random.get_state()
        temp = in_train_binary[signal_num]
        np.random.shuffle(temp)
        in_train_binary[signal_num] = temp

        np.random.set_state(rng_state)

        temp = out_train_binary[signal_num]
        np.random.shuffle(temp)
        out_train_binary[signal_num] = temp

        #Validation Data
        signal_num = 0
        for signal_num in range(0,5):
            i = 0
            j = 0
            for i in range(0,num_tests*100):
                in_test_binary[signal_num,i] = in_test[signal_num,i]
                out_test_binary[signal_num,i] = 1

            for j in range(num_tests*100,num_tests*200):
                rand_signal_num = signal_num
                while (rand_signal_num == signal_num):
                    rand_signal_num = randint(0,4)

                in_test_binary[signal_num,j] = in_test[rand_signal_num,randint(0,num_tests*100-1)]
                out_test_binary[signal_num,j] = (signal_num == rand_signal_num)


            #shuffle around data
            rng_state = np.random.get_state()
            temp = in_test_binary[signal_num]
            np.random.shuffle(temp)
            in_test_binary[signal_num] = temp

            np.random.set_state(rng_state)

            temp = out_test_binary[signal_num]
            np.random.shuffle(temp)
            out_test_binary[signal_num] = temp


    # print('Resulting input vector shape: ')
    # print(in_train_binary[0].shape)
    # print('Resulting output vector shape: ')
    # print(out_train_binary[0].shape)
    # print('Example resulting input vecotr:')
    # print(in_train_binary[0])
    # print('Example resulting output vector:')
    # print(out_train_binary[0])
    return in_train_binary, out_train_binary, in_test_binary, out_test_binary
if __name__ == "__main__":
    doBinary = True
    print('Train a binary net [Y/n]:')
    if(sys.stdin.readline() == 'n\n'):
        doBinary = False

    if (doBinary):
        import BNet_1 as net
    else:
        import Net_2 as net

    while True:
        if(doBinary):
            configFile = None
            if not (itrain.size and otrain.size and itest.size and otest.size):
                itrain, otrain, itest, otest = loadDataBinary('samples','tests')

            print('Enter to train 5 copies of BNet_1.py (x to exit): ')

            if(sys.stdin.readline() == 'x\n'): #exit loop
               sys.exit()

            net = imp.reload(net) #Reload net configuration
            try:
                i = 0
                for i in range(0,5):
                    net.train(itrain[i],otrain[i],itest[i],otest[i],'saved_nets/BNet_S' + str(i) + '_' + str(net_index))
                net_index = net_index+1
            except Exception as ex:
                print('Error in net: ',ex)
        else:
            if not (itrain.size and otrain.size and itest.size and otest.size):
                itrain, otrain, itest, otest = loadData('samples_even','tests_even')
                #print(itrain)
                print(otrain)
            print('Please enter to train Net2.py (x to exit): ')

            if(sys.stdin.readline() == 'x\n'): #exit loop
               sys.exit()

            net = imp.reload(net) #Reload net configuration
            try:
                net.train(itrain,otrain,itest,otest,'saved_nets/CatNet_' + str(net_index))
            except Exception as ex:
                print('Error in net: ',ex)
