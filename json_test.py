import os
import numpy
import numpy as np
import numpy as N
from numpy import genfromtxt
import random
import requests
import json
from pprint import pprint
import time

data = genfromtxt("mapbox.csv", delimiter=',',dtype=None)

name_column = data[:,0]

name_column = name_column.tolist()

wtf_index = []

# This function calls the Google Custom Search API of Google News to determine how many times a particular place was mentioned in the news.

for n in name_column:
    print n
    news = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyBUpGeo-j9MNW73kUDfSG2HxJwm5t8TQtw&cx=011812869797907996842%3Aczujyeamqbq&q="+n+"&start=1")
    news_reader = json.loads(news.text)
    print("Number of results")
    print(news_reader["searchInformation"]["totalResults"])
    wtf_index.append(news_reader["searchInformation"]["totalResults"])
    
    if int(news_reader["searchInformation"]["totalResults"]) != 0:
        print("Headline")
        print(news_reader["items"][0]["title"])
        print(news_reader["items"][0]["snippet"])
    else:
        print("No one knows what's going on in "+str(data))

print wtf_index

wtf_index = wtf_index[:]
data = [data[:,0],data[:,1],data[:,2],wtf_index]
data = zip(*data)

print data
numpy.savetxt("wtf_index.csv", data, delimiter=",", fmt="%s")

#
#n=-1
#place=[]
#while n >= -10:
#    location = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(data[n,1])+","+str(data[n,0])+"&radius=5000&key=AIzaSyBhDN2AqOqz_pccRm3YaRnAw1Ik4Ur-O6g")
#    #print location.json()
#    response = json.loads(location.text)
#    if response["status"] != "ZERO_RESULTS":
#        #print location.json()
#        print(response["results"][0]["vicinity"])
#        #print n
#        place.append(response["results"][0]["vicinity"])
#    else:
#    	print("There is no information available about this place.")
#    	#print n
#    	place.append("There is no information available about this place.")
#    n = n-1
#
#a = place[::-1]
#
#mapbox_array = []
#mapbox_array = [a,data[:,1],data[:,0],data[:,2]]
#mapbox_array = zip(*mapbox_array)
#header = ["title","lat","lon","intensity"]
#mapbox_array_header = numpy.vstack([header, mapbox_array])
#print mapbox_array_header
#numpy.savetxt("mapbox.csv", mapbox_array_header, delimiter=",", fmt="%s")
#
#
#length = N.shape(mapbox_array)[0]
#width = N.shape(mapbox_array)[1]
#
#print("the number of rows in mapbox is "+str(length))
#print("the number of columns in mapbox is "+str(width))