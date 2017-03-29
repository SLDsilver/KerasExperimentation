#Handles all data formatting and importation
import os
import numpy as np


input_id = 'sample'
output_id = 'mod'

#num_signal = number of files
#num_samples = number of samples per file
#directory = direccytory the data is kept in

def loadData(directory, num_signal, num_samples):
    temp_input = np.zeros(shape=(num_signal, num_samples*2))
    real_input = np.zeros(shape=(num_signal, num_samples))
    imag_input = np.zeros(shape=(num_signal, num_samples))
    ret_input = np.zeros(shape=(num_signal, num_samples, 2))
    temp_output = np.zeros(shape=(num_signal,1))

    counter = 0
    counter2 = 0

    print('Processing data')

    filecount = 0
    for filecount in range(0,num_signal):

        samples_filename = 'samples' + str(filecount) + '.txt'
        mod_filename = 'modScheme' + str(filecount) + '.txt'

        print('Currently processing: ' + samples_filename)

        temp_input[counter] = np.array(np.loadtxt(directory + "/" + samples_filename))

        i = 0
        j = 0
        while(j in range(0,temp_input.shape[1]-1)):
            #real_input[counter,i] = temp_input[counter,j]
            ret_input[counter,i,0] = temp_input[counter,j]
            j = j+1
            #imag_input[counter,i] = temp_input[counter,j]
            ret_input[counter,i,1] = temp_input[counter,j]
            j = j+1
            i = i+1

        temp_output[counter] = np.loadtxt(directory + "/" + mod_filename)
        counter = counter + 1


    print('Resulting input vector: ')
    print(ret_input)
    print('Resulting output vector: ')
    print(temp_output)
    return ret_input, temp_output
