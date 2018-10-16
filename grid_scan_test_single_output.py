import math
import pandas
import time
import csv
import os
import zipfile
import shutil
import glob
import sys
from osgeo import gdal




def extract_img_data(image_file):
    print(image_file)
    zip_ref = zipfile.ZipFile(image_file, 'r')
    zip_ref.extractall('temp_dir2')
    zip_ref.close()
    print("zip extracted")

    file = glob.glob('temp_dir2/*.img')[0]
    shutil.copy(file,"output2.img")
    print("img extracted")

    shutil.rmtree('temp_dir2')
    print("temp files deleted")



def get_elevation_array():
    img=gdal.Open("output2.img")
    inputArray=img.ReadAsArray()
    print("array extracted")
    return inputArray


def get_elevation_in_meters(elevation_array, lat, lng, boundingBox):
    #print(boundingBox)
    #print(lat)
    #print(lng)
    array_length = len(elevation_array)
    #print(array_length)

    y_range = boundingBox['maxY'] - boundingBox['minY']
    y_stop_length = y_range/array_length
    y_diff = boundingBox['maxY'] - (lat)
    y_stops = y_diff/y_stop_length

    x_range = boundingBox['maxX'] - boundingBox['minX']
    x_stop_length = x_range/array_length
    x_diff = lng - boundingBox['minX']
    x_stops = x_diff/x_stop_length
    if y_stops >= 0 and x_stops >= 0 and y_stops < array_length and x_stops < array_length:
        elevation = elevation_array[int(y_stops)][int(x_stops)]
        if elevation == -3.4028234663852886e+38:
            elevation = None
    else:
        elevation = None
    return elevation

def process_grid_square(image_file,road_file,bounding_box_string):


    boundingBox = {}
    for x in (bounding_box_string[1:-2].split(",")):
      boundingBox[x.split(":")[0]] = float(x.split(":")[1])

    print(boundingBox)
    extract_img_data(image_file)
    elevation_array = get_elevation_array()

    print(get_elevation_in_meters(elevation_array, 33, -85, boundingBox))

    pandas.options.mode.chained_assignment = None
    df = pandas.read_csv(road_file,
                            header=0,
                            names=['id','name','something','code','latitude','longitude','state','county'])
    #print(df)
    max_lat = (math.ceil(df['latitude'].max()))
    min_lat = (math.floor(df['latitude'].min()))
    max_lng = (math.ceil(df['longitude'].max()))
    min_lng = (math.floor(df['longitude'].min()))

    if abs(min_lng) < 100:
        zero_pad = "0"
    else:
        zero_pad = ""

    print(max_lat)
    print(min_lat)
    print(max_lng)
    print(min_lng)

    print("grid n%sw%s%s" % (int(max_lat),zero_pad,int(abs(min_lng))))
    print(df.state.unique())
    #print(df[df.state == 'GA'].sort_values(['a', 'b'], ascending=[True, False]))

    def get_elevation(row):
        return get_elevation_in_meters(elevation_array, row['latitude'], row['longitude'], boundingBox)

    #print(df.apply(get_elevation,axis=1))
    df['height'] = df.apply(get_elevation,axis=1)
    df['road_file'] = road_file.split("/")[-1]
    df['image_file'] = image_file.split("/")[-1]
    for state in df.state.unique():
        sorted = df[df.state == state].sort_values(['height'],ascending=[False])
        cols = ['height']
        #sorted[cols] = df[df[cols] > 0][cols]
        sorted = sorted.dropna(subset=cols)
        #print(sorted)
        #sorted.head(100).to_csv("final/%s_high.csv" % (state), mode='a', header=False)
        sorted.to_csv("final/%s_full_grid_to_check.csv" % (state), mode='a', header=False)
        print(sorted.tail(1).values)
def single_test():
    elevation_array = get_elevation_array()

    bounding_box_string = "{minY:32.99944444444,minX:-85.00055555556,maxY:34.00055555556,maxX:-83.99944444444}"
    boundingBox = {}
    for x in (bounding_box_string[1:-2].split(",")):
        boundingBox[x.split(":")[0]] = float(x.split(":")[1])

    lat = 33.977315999889825
    lng = -84.57929766694424

    print(get_elevation_in_meters(elevation_array, lat, lng, boundingBox))


master_df = pandas.read_csv("wyomingidaho.csv",
                        header=0)

for row in master_df.itertuples(index=True, name='Pandas'):
    bounding_box_string = getattr(row, "boundingbox")
    image_file = "/home/ed/Downloads/%s" % (getattr(row, "image_file"))
    road_file = "grids/%s" % getattr(row, "road_file")
    try:
        process_grid_square(image_file,road_file,bounding_box_string)

    except:
        continue
