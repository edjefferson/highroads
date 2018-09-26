import csv
import pandas
import math
import time
import os

files = sorted(os.listdir('grids'))

df = pandas.read_csv("coded_master_list_ned_img.csv",
                        header=0)

print(df)
for file in files:
    if file[-4:] == ".csv":
        print(file)
        start, end = file[:-4].split("w")
        new_start = int(start[1:]) + 1
        code = "n%sw%s" % (new_start,end)
        print(df[df.code == code].shape[0])
