## 1. First create a Dockerfile with this command in this directory


```docker build -t test:pandas .```

## 2. You can now run the container with this command (Use "winpty" if you are using bash on Windows)

```winpty docker run -it test:pandas```

## 3. Create pipeline.py and copy the original to the container

```winpty docker build -t test:pandas .```

## 4. Do some stuff in the container, change ENTRY bash to python, pipeline.py and the run it again
## 5. Create a postgreSQL connection. Configurate the docker image copying it in the github repository.

```
 winpty docker run -it  -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root"\
    -e POSTGRES_DB="ny_taxi"\
    -v C://Users//User//Desktop//Github//zoomcamp-by-me//week_1_basics_n_setup//2_docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432  postgres:13
 ```
## 6. Make sure that you put -v parameter in the docker run command (to mount the postgreSQL database)

## 7. Install pgcli with pip.Connect to DB with the command
```
    pgcli -h localhost -p 5432 -U root -d ny_taxi
```
## 8. Test the connection, do some stuffs like:
```
\dt
SELECT 1

```
## 9. Open a Jupyter notebook and download the data from (use wget)
```
https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```
## 10. Do some stuffs on the Jupyter-notebook.

## 11. Connect pgAdmin and Postgres using Docker
``` 
    winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4

```
## 12. We need to connect the database image to the pgadmin4 container. We can use a network. Create a network as
```
    docker network create pg-network
```
## 13. And the run the following sentence
```
    winpty docker run -it  -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C://Users//User//Desktop//Github//zoomcamp-by-me//week_1_basics_n_setup//2_docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 \
    --network=pg-network
    --name pg-database \
    postgres:13
    
```
## and
```
    winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
    
```
## You'll see the containers running. Just as this image:
    ![image](.\Docker-containers running.PNG)

## 14. Convert the jupyter notebook into a python script.
```
    jupyter nbconvert --to=script upload-data.ipynb
```
## 15. Use argparse to parse the arguments.
```
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to the file", type=str)
    args = parser.parse_args()
    print(args.file)
```

## 16. Add main to the python script.

## 17. Drop yellow_taxi data from postgres and then try the python script
```
URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trip \
  --url=${URL}

```
## 18. Make sure that everything is working with the following command
```
    $? is a built-in variable that stores the exit status of a command, function, or the script itself.

    $? reads the exit status of the last command executed. After a function returns, $? gives the exit status of the last command executed in the function. This is Bash's way of giving functions a "return value." It returns 0 on success or an integer in the range 1 - 255 on error.
```
## 19. Dockerizing Ingestion Script
```
    docker built -t taxi_ingest:v001 .
```
## 20 . Run Python script with docker image
```
    winpty docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pg-database \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trip \
  --url=${URL}
```
## 21. You could see your files in a local server using the following command
```
    python -m http.server
```
## 22. Find your IP address using the following command
```
    ipconfig
```
## 23. Open a browser and go to your IP address and port 8000. Then you can see the files in the local server.

## 24. Instead of using network we could use docker compose.
``` 
    docker-compose up -d
```
## 25. To shut down the containers use the following command
```
    docker-compose down
```
