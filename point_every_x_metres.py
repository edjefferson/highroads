from geographiclib.geodesic import Geodesic
import math
import pandas
import time
import csv
import os

geod = Geodesic.WGS84  # define the WGS84 ellipsoid



def stopsBetweenPoints(one, two, row):
    stops_array = []
    vector =  geod.Inverse(one[0], one[1], two[0], two[1])

    distance = (vector['s12'])
    heading = vector['azi1']
    stops = math.ceil(distance/10)
    stop_distance = distance/stops

    for i in range(1,stops + 1):
        stop = geod.Direct(one[0],one[1], heading, i * stop_distance)
        stops_array.append([row.id,row.name,row.something,row.code,stop['lat2'], stop['lon2']])
    return stops_array

def find_inbetween_points(file):
    output_file_name = file.split(".")[0] + "_result.csv"
    with open(output_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)

        df = pandas.read_csv(file,
                    header=0,
                    names=['id','name','something','code','latitude','longitude'])
        length = df.shape[0]
        x = 0
        last_row = None
        for row in df.itertuples(index=True, name='Pandas'):
            x += 1
            print("%s/%s" % (x, length), end='\r')
            if last_row and row.id == last_row.id:
                stops = stopsBetweenPoints([last_row.latitude,last_row.longitude],[row.latitude,row.longitude],row)
                for stop in stops:
                    csv_writer.writerow(stop)

            else:
                csv_writer.writerow([row.id,row.name,row.something,row.code,row.latitude,row.longitude])
            last_row = row

files = sorted(os.listdir('all_roads_csvs'))
for file in files:
    print(file)
    find_inbetween_points('all_roads_csvs/' + file)
