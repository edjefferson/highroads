import csv
import pandas
import math
import time
import os

def assign_to_grid(file_name):
    pandas.options.mode.chained_assignment = None
    df = pandas.read_csv(file_name,
                            header=0,
                            names=['id','name','something','code','latitude','longitude'])

    state = file_name.split("/")[-1].split("_")[0]
    county = file_name.split("/")[-1].split("_")[-2]
    #print(state)
    df['State'] = state
    #print(county)
    df['County'] = county
    df['longitude'] = df['longitude'].abs() * -1
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
        if abs(lng) < 100:
            zero_pad = "0"
        else:
            zero_pad = ""


        queried = df.query('latitude >= @lat & latitude < @lat + 1 & longitude >= @lng & longitude < @lng + 1')
        if queried.size > 0:
            queried['State'] = state
            queried.sort_values(by=['latitude','longitude']).to_csv("grids/n%sw%s%s.csv" % (lat,zero_pad,abs(lng)), mode='a', header=False)


            print("grid n%sw%s%s" % (lat,zero_pad,abs(lng)))

files = sorted(os.listdir('output/all_roads_csvs/'))

for file in files:
    if file[-4:] == ".csv": #and file[:2] <= "TN":
        print(file)
        assign_to_grid('output/all_roads_csvs/' + file)
        #time.sleep(5)


#("nytest.csv")
