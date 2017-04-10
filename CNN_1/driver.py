import load_data as ld
import imp
import runTHIS as rT
import sys
if __name__ == "__main__":
    #Load the data
    train_directory = 'samples' #["samples_0", "samples_1", "samples_2", "samples_3", "samples_4"]
    model_file = 'model_2C.h5'

    #Configuration: DO NOT MODIFY
    signal_size = 10000
    num_folder = 5
    depth = 2
    #Configuration: CAN MODIFY
    num_signal_folder = 1000
    signal_fragment_size = 1000
    test_directory = 'valid'
    test_num = 20

    # Data Importation
    # Load the training tuple
    train_x, train_y = ld.loadDataCancer(train_directory, num_signal_folder, signal_size, signal_fragment_size)

    # Load the validation tuple
    test_x, test_y = ld.loadDataCancer(test_directory, test_num, signal_size, signal_fragment_size)
    num_signals = test_y.shape[1]

    testing = True
    #Loop model
    while testing:
        rT = imp.reload(rT)
        model = rT.catergorical_model(signal_fragment_size, num_signals, depth)
        rT.activate(model, train_x, train_y, test_x, test_y)
        print('Do you wish to test further? Enter n to terminate.\n')
        if (sys.stdin.readline() == 'n\n'):
            testing = False


