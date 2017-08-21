import os
import numpy
import numpy as np
import numpy as N
from numpy import genfromtxt
import random
import requests
import json
import time

# This function imports an image from within the directory that the script is run.
def import_image():

    image_variable = str(random.randint(1, 10000))

    image_name = raw_input("Which scene would you like to analyze? Note that it must be in this root directory.")

    # Clip the image to remove poles and oceans
    os.system("gdalwarp -q -cutline /Users/daniel/Documents/Hackathon/Clipper.shp -crop_to_cutline -dstalpha -tr 0.1 0.1 -of GTiff /Users/daniel/Documents/Hackathon/"+image_name+" /Users/daniel/Documents/Hackathon/"+image_variable+".tif")

    # Turn the tiff into a text file
    os.system("gdal_translate -of XYZ /Users/daniel/Documents/Hackathon/"+image_variable+".tif /Users/daniel/Documents/Hackathon/"+image_variable+".xyz")
    
    data = genfromtxt(image_variable+".xyz", delimiter=' ')

    return data

# This function turns the image into a array and sorts by intensity.

def sort_by_intensity(data):

    data = np.array(data)

    data = data[data[:,2].argsort()]

    # This function writes the n most intense rows to a csv

    number_of_entries = raw_input("How many entries do you want to return?")

    data = data[-int(number_of_entries):,:]

    numpy.savetxt("sorted_data.csv", data, delimiter=",")
 
# This function loops over the array, calls the Google Places API, and appends the name as another column.
    n=-1
    place=[]

    while n >= -int(number_of_entries):
        location = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(data[n,1])+","+str(data[n,0])+"&radius=5000&key=AIzaSyBhDN2AqOqz_pccRm3YaRnAw1Ik4Ur-O6g")
        #print location.json()
        response = json.loads(location.text)
        if response["status"] != "ZERO_RESULTS":
            #print location.json()
            print(response["results"][0]["vicinity"])
            #print n
            place.append(response["results"][0]["vicinity"].encode('ascii', 'ignore').decode('ascii'))
        else:
            print("There is no information available about this place.")
            #print n
            place.append("There is no information available about this place.")
        n = n-1
    
    a = place[::-1]
    
    mapbox_array = []
    mapbox_array = [a,data[:,1],data[:,0],data[:,2]]
    mapbox_array = zip(*mapbox_array)
    header = ["title","lat","lon","intensity"]
    mapbox_array_header = numpy.vstack([header, mapbox_array])
    print mapbox_array_header
    #yourstring.encode('ascii', 'ignore').decode('ascii')
    numpy.savetxt("mapbox.csv", mapbox_array_header, delimiter=",", fmt="%s")
    
    
    #length = N.shape(mapbox_array)[0]
    #width = N.shape(mapbox_array)[1]
    #
    #print("the number of rows in mapbox is "+str(length))
    #print("the number of columns in mapbox is "+str(width))




#def call_places_api(data):
#    length = N.shape(data)[0]
#
#    print length
#
#    #print data[-1,1]
#
#    #print data[-1,0]
#    n=-1
#    place=[]
#    while n > -10:
#        location = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(data[n,1])+","+str(data[n,0])+"&radius=5000&key=AIzaSyBhDN2AqOqz_pccRm3YaRnAw1Ik4Ur-O6g")
#        print location.json()
#        json.loads(location.text)
#        print(data["results"][0]["vicinity"])
#        place[abs(n)] = data["results"][0]["vicinity"]
#        time.sleep(2)
#        n = n-1
#    print place
#    #return data
#
#def parse_json(location):
#
#    data = json.loads(location.text)
#
#    #print data
#
#    print(data["results"][0]["vicinity"])
#
#    place = data["results"][0]["vicinity"]
#
#    return place
#
#	#data = json.load(location.text)
#	#print(data["results"][0]["vicinity"])

def google_custom_search(data):
	
    news = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyBUpGeo-j9MNW73kUDfSG2HxJwm5t8TQtw&cx=011812869797907996842%3Aczujyeamqbq&q="+data+"&start=1")
    news_reader = json.loads(news.text)
    print("Number of results")
    print(news_reader["searchInformation"]["totalResults"])
    
    if int(news_reader["searchInformation"]["totalResults"]) != 0:
        print("Headline")
        print(news_reader["items"][0]["title"])
        print(news_reader["items"][0]["snippet"])
    else:
        print("No one knows what's going on in "+data)


sort_by_intensity(import_image())
#google_custom_search(parse_json(call_places_api(sort_by_intensity(import_image()))))



#with open('test.json') as data_file:    
 #   data = json.load(data_file)

#print(data["results"][0]["vicinity"])