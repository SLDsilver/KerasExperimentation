#Handles all data formatting and importation
import os
import numpy as np
import re
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
'''
#Allows you specify how much the directory you wish to train against
def loadData(directory, num_signal, num_samples, percentage):
    temp_input = np.zeros(shape=(num_signal*percentage), num_samples*2))
    temp_output = np.zeroes(shape=(int(num_signal*percentage), 1))'''


            
            
