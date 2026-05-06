import sys
print(sys.executable)

import pandas as pd
import kagglehub
import os
from tqdm import tqdm
# Download latest version
path = kagglehub.dataset_download("vrindakallu/new-york-dataset")

print("Path to dataset files:", path)

os.listdir(path)

csv_file = os.path.join(path, "new_york_listings_2024.csv")
df = pd.read_csv(csv_file)

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://airbnb:airbnb@localhost:5432/airbnb_data')

print(pd.io.sql.get_schema(df, name='new_york_listings', con=engine))

df.to_sql(name='new_york_listings', con=engine, if_exists='replace')

df_iter = pd.read_csv(
    csv_file,
    chunksize=1000
)

for df_chunk in df_iter:
    print(len(df_chunk))

df_chunk.to_sql(name='new_york_listings', con=engine, if_exists='append')

first = True

for df_chunk in df_iter:
    #Create table schema (no data)
    if first:
        df_chunk.head(0).to_sql(name='new_york_listings', con=engine, if_exists='replace')
        first = False

        #Insert data in chunks
    df_chunk.to_sql(name='new_york_listings', con=engine, if_exists='append')

    print(f"Inserted {len(df_chunk)} rows")


for df_chunk in tqdm(df_iter, desc="Inserting data"):
    ...

