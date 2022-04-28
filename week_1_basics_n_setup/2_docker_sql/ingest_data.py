#!/usr/bin/env python
# coding: utf-8
from time import time 
import pandas as pd
from sqlalchemy import create_engine

#Create PostgresSQl connection
engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
#Insert as a chunk
df_iter= pd.read_csv('yellow_tripdata_2021-01.csv', iterator = True, chunksize = 100000)

df = next(df_iter)

df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)


df.head(n=0).to_sql(name = 'yellow_taxi_data', con = engine, if_exists = 'replace')

while True:
    t_start = time()
    df = next(df_iter)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.to_sql(name = 'yellow_taxi_data', con = engine, if_exists = 'append')
    t_end = time()
    print('inserted another chunk..., took %.3f second' % (t_end-t_start))
    
    




