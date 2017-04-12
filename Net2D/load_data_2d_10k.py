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
    ret_input = np.zeros(shape=(num_signal, num_samples, 2))
    temp_output = np.zeros(shape=(num_signal,1))

    counter = 0
    out_counter = 0

    #print('Processing data')

    filecount = 0
    for filecount in range(0,num_signal):

        samples_filename = 'samples' + str(filecount) + '.txt'
        mod_filename = 'modScheme' + str(filecount) + '.txt'

        print('Currently processing: ' + samples_filename)

        temp_input = np.array(np.loadtxt(directory + "/" + samples_filename))

        j = 0 #temp_input column counter
        k = 0
        while(j in range(0, (num_samples*2)-1)):
            ret_input[filecount,k,0] = temp_input[j] + 5
            j = j+1
            ret_input[filecount,k,1] = temp_input[j] + 5
            j = j+1
            k = k+1

        temp_output[out_counter] = np.loadtxt(directory + "/" + mod_filename)
        out_counter = out_counter+1

    rng_state = np.random.get_state()
    np.random.shuffle(ret_input)
    np.random.set_state(rng_state)
    np.random.shuffle(temp_output)

    new_out = np.array(temp_output).reshape(num_signal,1)
    print(new_out)

    return np.array(ret_input).reshape(num_signal, num_samples, 2,1), new_out
