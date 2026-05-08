echo "# airbnb_data_flow" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mutaivictor263-ui/airbnb_data_flow.git
git push -u origin main


## Ingest script:
params

pg_user = airbnb
pg_pass = airbnb
pg_host = localhost
pg_db = airbnb_data
pg_port = 5432

chunk_size = 1000 (optional)
target-table = new_york_listings

### execute the ingestion scirpt using the following commands:

###### Use all defaults
uv run python ingest_data.py

###### Overide specific parameters
uv run python ingest_data.py \
  --pg-user=airbnb \
  --pg-password=airbnb \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=airbnb_data \
  --target-table=new_york_listings

###### See all available options 
uv run python ingest_data.py --help