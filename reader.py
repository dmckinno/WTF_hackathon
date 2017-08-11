import os
import numpy as np
import numpy as N
from numpy import genfromtxt
import random

####################################################
# This will be refactored into our image function

image_variable = str(random.randint(1, 10000))

image_name = raw_input("Which scene would you like to analyze? Note that it must be in this root directory.")

# Clip the image to remove poles and oceans
os.system("gdalwarp -q -cutline /Users/daniel/Documents/Hackathon/Clipper.shp -crop_to_cutline -dstalpha -tr 0.1 0.1 -of GTiff /Users/daniel/Documents/Hackathon/"+image_name+" /Users/daniel/Documents/Hackathon/"+image_variable+".tif")

# Turn the tiff into a text file
os.system("gdal_translate -of XYZ /Users/daniel/Documents/Hackathon/"+image_variable+".tif /Users/daniel/Documents/Hackathon/"+image_variable+".xyz")

# This is the end of our image function
####################################################



####################################################
# This will be refactored into our sorting function

data = genfromtxt(image_variable+".xyz", delimiter=' ')

data = np.array(data)

data = data[data[:,2].argsort()]

#print data

print data[-100:,:]

# This is the end of our sorting function
####################################################

####################################################
# This will be our pole filtering function
length = N.shape(data)[0]

n=0

for n in range(0,length):
	if abs(data[n,1]) > 70:
	    np.delete(data, n, 0)
	    n = n+1
	
print data[-100:,:]

new_length = N.shape(data)[0]

print length

print new_length

# This is the end of our pole filtering function
####################################################