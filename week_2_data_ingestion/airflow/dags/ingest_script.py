from time import time 
import pandas as pd
from sqlalchemy import create_engine
import os 

def ingest_callable(user, password, port,host, db, table_name, csv_file):

    #Create PostgresSQl connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    #Insert as a chunk
    df_iter= pd.read_csv(csv_file, iterator = True, chunksize = 100000)

    df = next(df_iter)
    if "yellow" in table_name:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    elif "fhv":
        df.pickup_datetime = pd.to_datetime(df.pickup_datetime)
        df.dropoff_datetime = pd.to_datetime(df.dropoff_datetime)
    else:
        raise ValueError("Unrecognized table name")


    df.head(n=0).to_sql(name = table_name, con = engine, if_exists = 'replace')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            if "yellow" in table_name:
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            elif "fhv" in table_name:
                df.pickup_datetime = pd.to_datetime(df.pickup_datetime, format='%Y-%m-%d %H:%M:%S')
                df.dropoff_datetime = pd.to_datetime(df.dropoff_datetime, format='%Y-%m-%d %H:%M:%S')
            else:
                raise ValueError("Unrecognized table name")
            df.to_sql(name =table_name, con = engine, if_exists = 'append')
            t_end = time()
            print('inserted another chunk..., took %.3f second' % (t_end-t_start))
        except StopIteration:
            print('Completed')
            break


    
    