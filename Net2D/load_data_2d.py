#Handles all data formatting and importation
import os
import numpy as np
from joblib import Parallel, delayed
import multiprocessing

input_id = 'sample'
output_id = 'mod'
num_cores = multiprocessing.cpu_count()

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

    #print('Processing data')

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

    return np.array(ret_input).reshape(num_signal*100, num_samples/100, 2,1), np.array(temp_output).reshape(num_signal*100,1)


def readDataSplit(directory, num_signal, num_samples, spf, counter):
    temp_input = np.zeros(num_samples*2)
    ret = np.zeros(shape=(spf+1, num_samples/spf, 2))

    samples_filename = 'samples' + str(counter) + '.txt'
    mod_filename = 'modScheme' + str(counter) + '.txt'

    print('Currently processing: ' + samples_filename)

    temp_input = np.array(np.loadtxt(directory + "/" + samples_filename))

    subrow_counter = 0
    subelement_counter = 0
    j = 0

    # for j in range(20000-1):
    #     if(subelement_counter >= spf):
    #         subelement_counter = 0
    #         subrow_counter = subrow_counter+1
    #         if(subrow_counter >= spf):
    #             break
    #
    #     ret[subrow_counter,subelement_counter,0] = temp_input[j]
    #     j = j+1
    #
    #     ret[subrow_counter,subelement_counter,1] = temp_input[j]
    #     j = j+1
    #
    #     subelement_counter = subelement_counter+1
    while(j in range(0,temp_input.shape[0]-1)):
        if(subelement_counter >= 100):
            subelement_counter = 0
            subrow_counter = subrow_counter+1

        ret[subrow_counter,subelement_counter,0] = temp_input[j]
        j = j+1
        ret[subrow_counter,subelement_counter,1] = temp_input[j]
        j = j+1

        subelement_counter = subelement_counter+1

    ret[spf,0,0] = counter
    return ret

def loadDataSplit(directory, num_signal, num_samples, spf):
    print("Loading data using " + str(num_cores) + " cores")
    ret_input = np.zeros(shape=(num_signal*spf, num_samples/spf, 2))
    temp_output = np.zeros(shape=(num_signal*spf,1))
    indicies = range(num_signal)

    #Paralellize reading inputs
    signal_segments = Parallel(n_jobs=num_cores)(delayed(readDataSplit)(directory, num_signal, num_samples, spf, i) for i in indicies)
    signal_segments = np.array(signal_segments)

    start_index = 0
    end_index = 0 + signal_segments.shape[1]-1
    for i in range(signal_segments.shape[0]):
        start_index = signal_segments[i,spf,0,0] * (signal_segments.shape[1] - 1)
        end_index = start_index + signal_segments.shape[1]-1

        for j in range(signal_segments.shape[1]-1):
            ret_input[int(start_index)+j] = np.array(signal_segments[i,j])



    #print(ret_input)
    #Standard read in outputs
    filecount = 0
    out_counter = 0
    for filecount in range(0,num_signal):
        mod_filename = 'modScheme' + str(filecount) + '.txt'
        k = 0
        for k in range(0,spf):
            temp_output[out_counter] = np.loadtxt(directory + "/" + mod_filename)
            out_counter = out_counter+1

    print('shuffling data')
    rng_state = np.random.get_state()
    np.random.shuffle(ret_input)
    np.random.set_state(rng_state)
    np.random.shuffle(temp_output)

    #print(ret_input.shape)

    return np.array(ret_input).reshape(num_signal*spf, num_samples/spf, 2,1), np.array(temp_output).reshape(num_signal*spf,1)
