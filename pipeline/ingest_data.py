#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine






dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "ehail_fee": "float64",       # present in this dataset
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "trip_type": "Int64",         # present in this dataset
}






parse_dates = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]












def run ():
    pg_user = "root"
    pg_pass = "root"
    pg_host = "localhost"
    pg_port = "5432"
    pg_db = "ny_taxi"
    table_name = "green_taxi_trips"
    year = 2019
    month = 1
    chunksize = 100000

    prefix =  'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green'
    url = f'{prefix}/green_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True ,
        chunksize=10000
    )


    first = True
    for df_chunk  in tqdm(df_iter): 
        if first:
            df_chunk.head(0).to_sql(
                name=f'{table_name}',
                con=engine ,
                if_exists='replace' 
            )
            first = False

        df_chunk.to_sql(name=f'{table_name}',
                        con=engine ,
                        if_exists='append'
        )

if __name__ == "__main__":
    run()
# In[ ]:




