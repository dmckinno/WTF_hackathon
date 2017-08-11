import numpy as np
from numpy import genfromtxt

data = genfromtxt('test.csv', delimiter=',')

data = np.array(data)

#print data

print data[-10:,:]

data = data[data[:,2].argsort()]

#print data

print data[-10:,:]