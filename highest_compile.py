import math
import pandas
import time
import csv
import os
import zipfile
import shutil
import glob
import sys

master_df = pandas.read_csv("statecodes.csv",
                        header=0)

columns = ['high_low','id_old','name','something','code','latitude','longitude','state','county','height','roadfile','nedfile']
df = pandas.DataFrame(columns=columns)



for row in master_df.itertuples(index=True, name='Pandas'):
    try:
        state_code = getattr(row, "code")
        high_df = pandas.read_csv("final/%s_high.csv" % (state_code),
                                header=0,
                                names=['id_old','name','something','code','latitude','longitude','state','county','height','roadfile','nedfile'])
        high_df['high_low'] = "high"
        #print(high_df.sort_values('height', ascending=False)[:1].values)
        high = high_df.sort_values('height', ascending=False)[:1]

        df = df.append(high, sort=True)

        low_df = pandas.read_csv("final/%s_low.csv" % (state_code),
                                header=0,
                                names=['id_old','name','something','code','latitude','longitude','state','county','height','roadfile','nedfile'])
        low_df['high_low'] = "low"

        cols = ['height']
        df[cols] = df[df[cols] > 0][cols]
        df = df.dropna(subset=['height'])
        low = low_df.sort_values('height', ascending=True)[:1]
        df = df.append(low, sort=True)
        #print(low_df.sort_values('height', ascending=True)[-1:].values)

    except:
        print("bum")
print(df)
df.to_csv("final_test.csv" , mode='w', header=True)
