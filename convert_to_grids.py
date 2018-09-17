import csv
import pandas
import math
import time
import os

def assign_to_grid(file_name):
    df = pandas.read_csv(file_name,
                            header=0,
                            names=['id','name','something','code','latitude','longitude'])



    max_lat = (math.floor(df['latitude'].max()))
    min_lat = (math.floor(df['latitude'].min()))
    max_lng = (math.floor(df['longitude'].max()))
    min_lng = (math.floor(df['longitude'].min()))

    lats = (list(range(min_lat, max_lat + 1)))
    lngs =(list(range(min_lng, max_lng + 1)))

    lat_lngs = []
    for lat in lats:
        for lng in lngs:
            lat_lngs.append([lat,lng])

    for lat, lng in lat_lngs:
        if lng > -100 or lng < 100:
            zero_pad = "0"
        else:
            zero_pad = ""
        queried = df.query('latitude >= @lat & latitude < @lat + 1 & longitude >= @lng & longitude < @lng + 1')
        if queried.size > 0:
            queried.sort_values(by=['latitude','longitude']).to_csv("grids/n%sw%s%s.csv" % (lat,zero_pad,-lng), mode='a', header=False)


            print("grid n%sw%s%s" % (lat,zero_pad,-abs(lng)))

files = sorted(os.listdir('output/all_roads_csvs/'))

for file in files:
    if file[-4:] == ".csv" and file[:2] <= "LA":
        print(file)
        assign_to_grid('output/all_roads_csvs/' + file)
        #time.sleep(5)


#("nytest.csv")
