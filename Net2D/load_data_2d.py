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
    ret_input = np.zeros(shape=(num_signal*100, num_samples/100, 2))
    temp_output = np.zeros(shape=(num_signal*100,1))

    counter = 0
    subrow_counter = 0
    out_counter = 0

    print('Processing data')

    filecount = 0
    for filecount in range(0,num_signal):

        samples_filename = 'samples' + str(filecount) + '.txt'
        mod_filename = 'modScheme' + str(filecount) + '.txt'

        print('Currently processing: ' + samples_filename)

        temp_input[counter] = np.array(np.loadtxt(directory + "/" + samples_filename))

        j = 0 #temp_input column counter
        subelement_counter = 0

        while(j in range(0,temp_input.shape[1]-1)):
            if(subelement_counter >= 100):
                subelement_counter = 0
                subrow_counter = subrow_counter+1

            ret_input[subrow_counter,subelement_counter,0] = temp_input[counter,j]
            j = j+1
            ret_input[subrow_counter,subelement_counter,1] = temp_input[counter,j]
            j = j+1

            subelement_counter = subelement_counter+1


        k = 0
        for k in range(0,100):
            temp_output[out_counter] = np.loadtxt(directory + "/" + mod_filename)
            out_counter = out_counter+1
        counter = counter + 1

    print('shuffling data')
    rng_state = np.random.get_state()
    np.random.shuffle(ret_input)
    np.random.set_state(rng_state)
    np.random.shuffle(temp_output)


    print('Resulting input vector shape: ')
    print(ret_input.shape)
    print('Resulting output vector shape: ')
    print(temp_output.shape)
    return ret_input, temp_output
