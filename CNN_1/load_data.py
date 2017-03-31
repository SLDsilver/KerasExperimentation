#Handles all data formatting and importation
import os
import numpy as np
import re
import random
input_id = 'samples'
output_id = 'modScheme'
#Default form
#Converts raw data into
#input = numpy array of vectors of the entire length
#i.e. array([[1 2 3 ...], [1 2 3 ...], ...])
# array.length = number of signals
# vector content = real, imaginary, real , imaginary ...
#output = numpy array of the number of signals
#i.e. array([[1], [2], [3], ...])
def loadData(directory, num_signal, num_samples):
    temp_input = np.zeros(shape=(num_signal, num_samples*2))
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

#Desired Input Shape is (num_signal_total, num_size, 1)
def loadDataAlpha(directory, num_signal, num_samples, num_size):
    num_signal_total = num_signal * num_samples / num_size
    temp_input = np.zeros(shape=(num_signal_total, num_size))
    temp_output= np.zeros(shape=(num_signal_total, 1))
    positions = random.sample(range(num_signal_total), num_signal_total)
    counter = 0
    print('Processing data')
    for filename in os.listdir(directory):
        if input_id in filename:
            print('Currently processing: ' + filename)
            fileID = int(re.sub(r"\D", "", filename))
            temp_data = np.loadtxt(directory + "/" + filename)
            temp_sol = np.loadtxt(directory + "/" + output_id + str(fileID) + ".txt")
            temp_data = np.reshape(temp_data, (num_samples / num_size, num_size))
            for x in range(0, num_samples / num_size):
                temp_input[positions[counter]] = temp_data[x]
                temp_output[positions[counter]] = temp_sol
                counter = counter + 1
    print('Finished processing data')
    return temp_input, temp_output
            
                                  




            
            
