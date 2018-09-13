import csv
import pandas
import math


df = pandas.read_csv("nytest_result.csv",

            header=0,
            names=['id','name','something','code','latitude','longitude'])



#print(df.dtypes)
#queried = df.query('latitude > 40.7 & latitude < 40.8')
#print(queried.sort_values(by=['latitude','longitude']))
#queried.sort_values(by=['latitude','longitude']).to_csv("pandas.csv")
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
    queried = df.query('latitude >= @lat & latitude < @lat + 1 & longitude >= @lng & longitude < @lng + 1')
    queried.sort_values(by=['latitude','longitude']).to_csv("n%sw%s.csv" % (lat,-lng))
    print(queried)
print(lat_lngs)
