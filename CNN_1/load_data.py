#Handles all data formatting and importation
from keras.utils import np_utils

import os
import numpy as np
import re
import random

input_id = 'samples'
output_id = 'modScheme'
'''Default form
Converts raw data into
input = numpy array of vectors of the entire length
i.e. array([[1 2 3 ...], [1 2 3 ...], ...])
array.length = number of signals
vector content = real, imaginary, real , imaginary ...
output = numpy array of the number of signals
i.e. array([[1], [2], [3], ...])'''
def loadData(directory, num_signal, num_samples):
    temp_input = np.zeros(shape=(num_signal, num_samples))
    temp_output = np.zeros(shape=(num_signal, 1))
    print('Processing data')
    for filename in os.listdir(directory):
        print('Currently processing: ' + filename)
        if input_id in filename:
            location = int(re.sub(r"\D", "", filename))
            temp_input[location] = np.loadtxt(directory + "/" + filename)
        if output_id in filename:
            location = int(re.sub(r"\D", "", filename))
            temp_output[location] = np.loadtxt(directory + "/" + filename)
    #print('Resulting input vector: ')
    #print(temp_input)
    #print('Resulting output vector: ')
    #print(temp_output)
    return temp_input, temp_output

''' loadDataAlpha allows you to fragment the data
Desired Input Shape is (num_signal_total, num_size, 1)
num_signal = the number of signals you generated = # of samples.txt files
num_samples = the number of samples per a signal = 2x the sampling point
num_size = the size of the fragments
'''
def loadDataAlpha(directory, num_signal, num_samples, num_size, data_log = "dataLog.txt", log = False):
    num_signal_total = int(num_signal * num_samples / num_size) #Calculate the number of signal fragments total
    num_samples_set = int(num_samples / num_size)   #Calculate the number of signal fragments per a signal
    temp_input = np.zeros(shape=(num_signal_total, num_size))    #Initialize array
    temp_output= np.zeros(shape=(num_signal_total, 1))      #Initialize array
    positions = random.sample(range(num_signal_total), num_signal_total)    #List of random numbers
    counter = 0
    print('Processing data')
    for filename in os.listdir(directory):  #For each file in directory
        if input_id in filename:            #If it is a signal file
            #print('Currently processing: ' + filename)
            fileID = int(re.sub(r"\D", "", filename))   #Grab the signal number
            temp_data = np.loadtxt(directory + "/" + filename)  #Load the data
            temp_sol = np.loadtxt(directory + "/" + output_id + str(fileID) + ".txt")   #Load the data
            temp_data = np.reshape(temp_data, (num_samples_set, num_size)) #Shape data
            for x in range(0, num_samples_set):
                if(log):
                    manualValidate(data_log, positions[counter], filename, temp_sol, temp_data[x])
                temp_input[positions[counter]] = temp_data[x]
                temp_output[positions[counter]] = temp_sol
                counter = counter + 1
    print('Finished processing data')
    temp_input = np.array(temp_input).reshape(num_signal_total, num_size, 1)
    temp_output = np_utils.to_categorical(np.array(temp_output))
    print(temp_input.shape)
    print(temp_output.shape)
    
    return temp_input, temp_output

''' Returns data in the binary format
Preforms the same processing as loadDataAlpha except
You must pass the current signal type. It will set all other signal types to 0 '''
def loadDataBinary(directory, num_signal, num_samples, num_size, signal_type, data_log = "dataLog.txt", log = False):
    num_signal_total = int(num_signal * num_samples / num_size) #Calculate the number of signal fragments total
    num_samples_set = int(num_samples / num_size)   #Calculate the number of signal fragments per a signal
    temp_input = np.zeros(shape=(num_signal_total, num_size))    #Initialize array
    temp_output= np.zeros(shape=(num_signal_total, 1))      #Initialize array
    positions = random.sample(range(num_signal_total), num_signal_total)    #List of random numbers
    counter = 0
    print('Processing data')
    for filename in os.listdir(directory):  #For each file in directory
        if input_id in filename:            #If it is a signal file
            #print('Currently processing: ' + filename)
            fileID = int(re.sub(r"\D", "", filename))   #Grab the signal number
            temp_data = np.loadtxt(directory + "/" + filename)  #Load the data
            temp_sol = np.loadtxt(directory + "/" + output_id + str(fileID) + ".txt")   #Load the data
            temp_data = np.reshape(temp_data, (num_samples_set, num_size)) #Shape data
            for x in range(0, num_samples_set):
                temp_input[positions[counter]] = temp_data[x]
                if(temp_sol == signal_type):
                    temp_output[positions[counter]] = 1
                else:
                    temp_output[positions[counter]] = 0
                if(log):
                    manualValidate(data_log, positions[counter], filename, temp_output[positions[counter]], temp_data[x])
                counter = counter + 1
    print('Finished processing data')
    temp_input = np.array(temp_input).reshape(num_signal_total, num_size, 1)
    temp_output = np_utils.to_categorical(np.array(temp_output))

    return temp_input, temp_output

#Prints to terminal where a supposed signal data, signal type, and filename is
#for the user to verify that the data is correctly asscioated 
def manualValidate(data_log, position, filename, signal_type, data):
    with open(data_log, 'a+') as f:
        f.write("The position " + str(position) + " data comes from " + filename + "\t")
        f.write("Its corresponding signal type is " + str(signal_type))
        f.write("\n")
    



            
            
