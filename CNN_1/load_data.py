#Handles all data formatting and importation
import os
import numpy as np
input_id = 'sample'
output_id = 'mod'
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
    temp_output = np.zeroes(shape=(num_signal,
    counter = 0
    print('Processing data')
    for filename in os.listdir(directory):
        print('Currently processing: ' + filename)
        if input_id in filename:
            temp_input[counter] = np.loadtxt(directory + "/" + filename)
            counter = counter + 1
        if output_id in filename:
            temp_output = np.loadtxt(directory + "/" + filename)
    print('Resulting input vector: ')
    print(temp_input)
    print('Resulting output vector: ')
    print(temp_output)
    print('For debugging purposes:')
    print('Input Shape: ' + temp_input.shape)
    print('Output Shape: ' + temp_output.shape)
    return temp_input, temp_output

            
            
