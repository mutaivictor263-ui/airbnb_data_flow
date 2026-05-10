echo "# airbnb_data_flow" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mutaivictor263-ui/airbnb_data_flow.git
git push -u origin main


### Ingest script:
params

pg_user = airbnb
pg_pass = airbnb
pg_host = localhost
pg_db = airbnb_data
pg_port = 5432

chunk_size = 1000 (optional)
target-table = new_york_listings

### execute the ingestion scirpt using the following commands:

### Use all defaults
uv run python ingest_data.py

### Overide specific parameters
uv run python ingest_data.py \
  --pg-user=airbnb \
  --pg-password=airbnb \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=airbnb_data \
  --target-table=new_york_listings

### See all available options 
uv run python ingest_data.py --help

### run pgAdmin as a container with the postgres container
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="airbnb@newyork.com" \
  -e PGADMIN_DEFAULT_PASSWORD="airbnb" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4


### create a virtual docker network called pgbnb-network
docker network create pgbnb-network


### stop the previous containers and re-run them with the network configuration
### Run PostgreSQL on the network
docker run -it \
  -e POSTGRES_USER=airbnb \
  -e POSTGRES_PASSWORD=airbnb \
  -e POSTGRES_DB=airbnb_data \
  -p 5432:5432 \
   --name airbnb-postgres \
  --network=pgbnb-network \
  postgres:18

### In another terminal, run pgAdmin on the same network
  docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="airbnb@newyork.com" \
  -e PGADMIN_DEFAULT_PASSWORD="airbnb" \
  -v airbnb_pgadmin_data:/var/lib/pgadmin \
  -p 8092:80 \
  --network=pgbnb-network \
  --name airbnb-pgadmin \
  dpage/pgadmin4


### Build the Docker image
docker build -t airbnb_ingest:latest .

### run the containerized ingestion

  docker run -it \
    --network=pgbnb-network \
    airbnb_ingest:latest \
    --pg-user=airbnb \
    --pg-password=airbnb \
    --pg-host=airbnb-postgres \
    --pg-port=5432 \
    --pg-db=airbnb_data \
    --target-table=new_york_listings

