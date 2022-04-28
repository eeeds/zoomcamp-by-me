#!/usr/bin/env python
# coding: utf-8
from time import time 
import pandas as pd
from sqlalchemy import create_engine, table
import argparse
import os 

def main(params):
    user = params.user
    password = params.password
    port = params.port
    host= params.host
    db = params.db
    url = params.url
    table_name= params.table_name

    csv_name = 'output.csv'
    #Download csv file from url
    os.system(f"wget {url} -O {csv_name}")

    #Create PostgresSQl connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    #Insert as a chunk
    df_iter= pd.read_csv(csv_name, iterator = True, chunksize = 100000)

    df = next(df_iter)

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)


    df.head(n=0).to_sql(name = table_name, con = engine, if_exists = 'replace')

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.to_sql(name =table_name, con = engine, if_exists = 'append')
        t_end = time()
        print('inserted another chunk..., took %.3f second' % (t_end-t_start))

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to PostgreSQL')
    # user
    # password 
    # host
    # port
    # database name
    # table name
    # url of the csv 
    parser.add_argument('--user',help= 'user name for postgresql')
    parser.add_argument('--password',help= 'password for postgresql')
    parser.add_argument('--host',help= 'host name for postgresql')
    parser.add_argument('--port',help= 'port for postgresql')
    parser.add_argument('--db',help= 'database name for postgresql')
    parser.add_argument('--table_name',help= 'name of the table where we will write the results to')
    parser.add_argument('--url',help= 'url of the csv file')
    args = parser.parse_args()
    main(args)

    
    




