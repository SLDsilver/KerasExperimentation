from keras.models import Sequential
from keras.layers import Dense, Activation, Conv1D

import numpy as np
import correct_Complex as c


from pymatbridge import Matlab

#Communicates data extraction from Matlab
mlab = Matlab()
mlab.start()
mlab.run('toFile.m')

#Import the data 
c.correct_Complex('usabledata.txt', 'useThis.txt')
#Convert to numpy array
c.import_As_Numpy_Array('useThis.txt')


#How many features map (depth), filters
#Create the model
#model = Sequential()
#model.add(Convolution1D(input_shape=(,1000000), activation='relu',  
    
