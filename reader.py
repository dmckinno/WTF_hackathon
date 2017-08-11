import os
import numpy
import numpy as np
import numpy as N
from numpy import genfromtxt
import random
import requests
import json
from pprint import pprint



def import_image():

    image_variable = str(random.randint(1, 10000))

    image_name = raw_input("Which scene would you like to analyze? Note that it must be in this root directory.")

    # Clip the image to remove poles and oceans
    os.system("gdalwarp -q -cutline /Users/daniel/Documents/Hackathon/Clipper.shp -crop_to_cutline -dstalpha -tr 0.1 0.1 -of GTiff /Users/daniel/Documents/Hackathon/"+image_name+" /Users/daniel/Documents/Hackathon/"+image_variable+".tif")

    # Turn the tiff into a text file
    os.system("gdal_translate -of XYZ /Users/daniel/Documents/Hackathon/"+image_variable+".tif /Users/daniel/Documents/Hackathon/"+image_variable+".xyz")
    
    data = genfromtxt(image_variable+".xyz", delimiter=' ')

    return data

def sort_by_intensity(data):

    data = np.array(data)

    data = data[data[:,2].argsort()]

    #print data

    print data[-100:,:]

    number_of_entries = raw_input("How many entries do you want to return?")

    data_culled = data[-int(number_of_entries):,:]

    numpy.savetxt("sorted_data.csv", data_culled, delimiter=",")

    return data

def call_places_api(data):
    length = N.shape(data)[0]

    print length

    print data[-1,1]

    print data[-1,0]

    location = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(data[-15,1])+","+str(data[-15,0])+"&radius=10&key=AIzaSyBhDN2AqOqz_pccRm3YaRnAw1Ik4Ur-O6g")

    print location

    print location.json()


call_places_api(sort_by_intensity(import_image()))

#with open('test.json') as data_file:    
 #   data = json.load(data_file)

#pprint(data)

#data["name"]