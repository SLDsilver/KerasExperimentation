#Handles all data formatting and importation
from keras.utils import np_utils

import os
import sys
import numpy as np
import re
import random

input_id = 'samples'
output_id = 'modScheme'

''' loadDataAlpha allows you to fragment the data
Desired Input Shape is (num_signal_total, num_size, 1)
num_signal = the number of signals you generated = # of samples.txt files
num_samples = the number of samples per a signal = # of sampling points
num_size = the size of the fragments
'''
def loadDataAlpha(directory, num_size, data_log = "dataLog.txt", default_file_shape = 'samples0.txt', log = False):
    depth = 2
    temp_input, temp_output, num_signal_total, num_samples_set = extractAndInitalize(directory, default_file_shape, num_size, depth)
    positions = random.sample(range(num_signal_total), num_signal_total)    #List of random numbers
    counter = 0
    for filename in os.listdir(directory):  #For each file in directory
        if input_id in filename:            #If it is a signal file
            fileID = int(re.sub(r"\D", "", filename))   #Grab the signal number
            signalFileName = directory + '/' + filename
            modFileName = directory + '/' + output_id + str(fileID) + '.txt'
            temp_data = np.loadtxt(signalFileName)  #Load the data
            print('Finished Loading : ' + signalFileName)
            temp_sol = np.loadtxt(modFileName)   #Load the data
            print('Finished Loading: ' + modFileName)
            temp_data = np.reshape(temp_data, (num_samples_set, num_size, depth)) #Shape data
            for x in range(0, num_samples_set):
                if(log):
                    manualValidate(data_log, positions[counter], filename, temp_sol, temp_data[x])
                temp_input[positions[counter]] = temp_data[x]
                temp_output[positions[counter]] = temp_sol
                counter = counter + 1
    temp_input = np.array(temp_input)
    temp_output = np_utils.to_categorical(np.array(temp_output))
    print('Finished processing data')
    print(temp_input)
    print(temp_output)
    with open('dataInput.txt', 'wb') as f:
        np.savetxt(f, temp_input[1,...], newline='\n', delimiter='\n')
    with open('dataOutput.txt', 'wb') as f:
        np.savetxt(f, temp_output, newline='\n', delimiter='\n')
    return temp_input, temp_output

def autoValidate(w, test_file, check_file):
    #Find the w in test_file
    file = open(test_file, 'r')
    i = 0
    for line in file:
        line = line.rstrip('\n')
        if(float(line) == w[0]):
            print('Found the first value in the current signal fragment')
            
            
def extractAndInitalize(directory, default_file_shape, num_size, depth):
    print('Begin Data Processing!')
    print('------------------------------------------------------------------------------')
    print('Determining the number of files in directory')
    num_signal = len([name for name in os.listdir(directory) if input_id in name])
    print('Have determined there are: ' + str(num_signal) + ' signal files')
    num_solutions = len([name for name in os.listdir(directory) if output_id in name])
    print('Have determined there are: ' + str(num_solutions) + ' modSchemes')
    print('Asserting that the number of signals equals the number of solutions')
    if(num_signal != num_solutions):
        print('Assertion failed.')
        print('Check that the directory contains equal numbers of signal and solution files')
        print('Loading terminating.')
        return
    print('Extracting the number of sample points in a signal file: ' + default_file_shape)
    num_samples = np.loadtxt(directory + '/' + default_file_shape).shape[0] / 2
    print('Have determined there are: ' + str(num_samples) + ' sample points')
    num_signal_total = int(num_signal * num_samples / num_size) #Calculate the number of signal fragments total
    print('The number of signal fragments is: ' + str(num_signal_total))
    num_samples_set = int(num_samples / num_size)   #Calculate the number of signal fragments per a signal
    print('The number of signal fragments per file is: ' + str(num_samples_set))
    temp_input = np.zeros(shape=(num_signal_total, num_size, depth))    #Initialize array
    temp_input_shape = temp_input.shape
    print('The shape of the input vector is: ' + str(temp_input_shape[0]) + ' signal fragments containing ' +
          str(temp_input_shape[1]) + ' sample points containing ' + str(temp_input_shape[2]) + ' values.')
    temp_output= np.zeros(shape=(num_signal_total, 1))      #Initialize array
    temp_output_shape = temp_output.shape
    print('The shape of the output vector is: ' + str(temp_output_shape[0]) + ' modSchemes containing ' + str(temp_output_shape[1]) + ' value')
    print('Please verify this information. Enter n to terminate program.\n')
    if(sys.stdin.readline() == 'n\n'):
        return
    else:
        return temp_input, temp_output, num_signal_total, num_samples_set
    
    
''' loadDataCancer allows you to fragment the data
Desired Input Shape is (num_signal_total, num_size, 1)
num_signal = the number of signals you generated = # of samples.txt files
num_samples = the number of samples per a signal = # of sampling points
num_size = the size of the fragments
'''
def loadDataCancer(directory, num_signal, num_samples, num_size, data_log="dataLog.txt", log=False):
    num_signal_total = int(num_signal * num_samples / num_size)  # Calculate the number of signal fragments total
    num_samples_set = int(num_samples / num_size)  # Calculate the number of signal fragments per a signal
    temp_input = np.zeros(shape=(num_signal_total, num_size, 2))  # Initialize array
    temp_output = np.zeros(shape=(num_signal_total, 1))  # Initialize array
    positions = random.sample(range(num_signal_total), num_signal_total)  # List of random numbers
    counter = 0
    print('Processing data')
    for filename in os.listdir(directory):  # For each file in directory
        if input_id in filename:  # If it is a signal file
            print('Processing file:' + filename)
            fileID = int(re.sub(r"\D", "", filename))  # Grab the signal number
            temp_data = np.loadtxt(directory + "/" + filename)  # Load the data
            temp_sol = np.loadtxt(directory + "/" + output_id + str(fileID) + ".txt")  # Load the data
            temp_data = np.reshape(temp_data, (num_samples_set, num_size, 2))  # Shape data
            for x in range(0, num_samples_set):
                if (log):
                    manualValidate(data_log, positions[counter], filename, temp_sol, temp_data[x])
                temp_input[positions[counter]] = temp_data[x]
                temp_output[positions[counter]] = temp_sol
                counter = counter + 1
    print('Finished processing data')
    temp_input = np.array(temp_input)
    temp_output = np_utils.to_categorical(np.array(temp_output))

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
            print('Processing file:' + filename)
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


#Modifies to Binary
#Not yet tested
def modifyToBinary(data, signal_type):
    size = data.shape[0]
    temp_binary = np.zeros(shape=(size, 1))
    for x in range(0, temp_binary.shape[0]):
        for y in range(0, temp_binary.shape[1]):
            if data[0][signal_type] == 1:
                temp_binary[x] = 1
            else:
                temp_binary[y] = 0
    return temp_binary


def loadDataBeta(directory, num_dir, num_signal, num_samples, num_size, data_log="dataLog.txt", log=False):
    num_signal_total = int(num_signal * num_samples / num_size)  # Calculate the number of signal fragments total
    num_samples_set = int(num_samples / num_size)  # Calculate the number of signal fragments per a signal
    temp_input = np.zeros(shape=(num_signal_total*num_dir, num_size, 2))  # Initialize array
    temp_output = np.zeros(shape=(num_signal_total*num_dir, 1))  # Initialize array
    positions = random.sample(range(num_signal_total*num_dir), num_signal_total*num_dir)  # List of random numbers
    counter = 0
    print('Processing data')
    for folder in directory:    #For every folder
        for filename in os.listdir(folder):  # For each file in directory
            if input_id in filename:  # If it is a signal file
                fileID = int(re.sub(r"\D", "", filename))  # Grab the signal number
                str_file = folder + "/" + filename
                temp_data = np.loadtxt(str_file)  # Load the data
                temp_sol = np.loadtxt(folder + "/" + output_id + str(fileID) + ".txt")  # Load the data
                temp_data = np.reshape(temp_data, (num_samples_set, num_size, 2))  # Shape data
                for x in range(0, num_samples_set):
                    if (log):
                        manualValidate(data_log, positions[counter], filename, temp_sol, temp_data[x])
                    temp_input[positions[counter]] = temp_data[x]
                    temp_output[positions[counter]] = temp_sol
                    counter = counter + 1
    print('Finished processing data')
    temp_input = np.array(temp_input)
    temp_output = np_utils.to_categorical(np.array(temp_output))

    return temp_input, temp_output
    



            
            
