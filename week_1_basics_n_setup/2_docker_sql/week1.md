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
