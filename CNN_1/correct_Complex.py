#Helper script
#Converts into numpy array
import numpy as np

#Param: filename - the name of the file to extract data
#File contains data of form complex 64 bits
#Purpose: Takes file and converts it into a numpy array for processing
def correct_Complex(filename, outname):
    f = open(outname, "w+")
    with open(filename, 'r+') as text_file:
        for line in text_file:
            if "+ -" in line:
                f.write(line.replace("+ -", "-"))
            else:
                f.write(line.replace("+ ", "+"))
    f.close()


def import_As_Numpy_Array(filename):
    text_file = open(filename, 'r')
    array = text_file.read().split('\n')
    print(len(array))
    text_file.close()
    np_array = np.array(array)
    return np_array