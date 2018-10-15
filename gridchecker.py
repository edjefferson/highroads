import csv
import pandas
import math
import time
import os


def get_max_y(row):
    return float(row['boundingBox'].split("maxY:")[1].split(",")[0])

def get_min_y(row):
    return float(row['boundingBox'].split("minY:")[1].split(",")[0])

def get_max_x(row):
    return float(row['boundingBox'].split("maxX:")[1].split("}")[0])

def get_min_x(row):
    return float(row['boundingBox'].split("minX:")[1].split(",")[0])

def every_thing():
    files = sorted(os.listdir('grids'))

    df = pandas.read_csv("coded_master_list_alaska.csv",
                            header=0)

    df['maxY'] = df.apply(get_max_y,axis=1)
    df['minY'] = df.apply(get_min_y,axis=1)
    df['maxX'] = df.apply(get_max_x,axis=1)
    df['minX'] = df.apply(get_min_x,axis=1)

    with open('gridmatches_alaska.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for file in files:
            if file[-4:] == ".csv":


                file_df = pandas.read_csv("grids/" + file,

                                        names=['id','name','something','code','latitude','longitude','state','county'])

                max_lat = file_df['latitude'].max()
                min_lat = file_df['latitude'].min()
                max_lng = file_df['longitude'].max()
                min_lng = file_df['longitude'].min()

                matching_grid_squares = df.query("minY <= %s & maxY >= %s & minX <= %s & maxX >= %s" % (min_lat, max_lat,min_lng, max_lng))
                
                print file + ":" + str(matching_grid_squares.shape[0])
                for index, row in matching_grid_squares.iterrows():
                    csvwriter.writerow([file, file[:-4],row['code'],row['downloadURL'],row['boundingBox']])
                    print(file + "," + file[:-4] + "," + row['code'] + "," + row['downloadURL'] + "," + row['boundingBox'])



                start, end = file[:-4].split("w")
                new_start = int(start[1:]) + 1
                code = "n%sw%s" % (new_start,end)



def allfile():
    files = sorted(os.listdir('grids'))
    with open('allfiles.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for file in files:
            if file[-4:] == ".csv":
                csvwriter.writerow([file])

every_thing()
#allfile()
