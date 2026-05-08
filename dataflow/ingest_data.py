import sys
print(sys.executable)

import pandas as pd
import kagglehub
import os
import click
from sqlalchemy import create_engine


@click.command()
@click.option('--pg-user', default='airbnb', help='PostgreSQL username')
@click.option('--pg-password', default='airbnb', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='airbnb_data', help='PostgreSQL database name')
@click.option('--target-table', default='new_york_listings', help='Target table name')
def ingest_data(pg_user, pg_password, pg_host, pg_port, pg_db, target_table):
    """Ingest Airbnb New York dataset into PostgreSQL database."""

    # Download latest version
    path = kagglehub.dataset_download("vrindakallu/new-york-dataset")

    print("Path to dataset files:", path)

    csv_file = os.path.join(path, "new_york_listings_2024.csv")

    # Read full CSV
    df = pd.read_csv(csv_file)

    # Create PostgreSQL engine
    engine = create_engine(
        f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
    )

    print("Connected to PostgreSQL")

    # Show schema
    print(pd.io.sql.get_schema(df, name=target_table, con=engine))

    # Create table + insert all data
    df.to_sql(
        name=target_table,
        con=engine,
        if_exists='replace',
        index=False
    )

    print(f"Inserted {len(df)} rows into '{target_table}'")


if __name__ == "__main__":
    ingest_data()



"""
docker run -it
--rm \
--network=host \
-v /home/vrinda/airbnb_data:/app/data \
airbnb_dataflow:latest \
python ingest_data.py
"""

"""
docker run -it \
airbnb_data:latest \
--pg_user=airbnb \
--pg_password=airbnb \
--pg_host=pgdatabase \
--pg_port=5432 \
--pg_db=airbnb_data \
--target_table=new_york_listings \
python ingest_data.py
"""



#run  the script locally with different parameters
"""
# Use all defaults
python ingest_data.py

# Override specific parameters
python ingest_data.py --pg-user my_user --pg-password my_pass --pg-host db.example.com
or with uvicorn
uv run python ingest_data.py \
  --pg-user=airbnb \
  --pg-password=airbnb \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=airbnb_data \
  --target-table=new_york_listings

# See all available options
python ingest_data.py --help

"""
