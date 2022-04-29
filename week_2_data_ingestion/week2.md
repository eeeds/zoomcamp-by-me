## 1. First follow the pre_setup.md file for installing the airflow image from the official repo.
## 2. I will do with Postgresql (local).
## 3. Make sure that you have all folders tu run your docker-compose file. Then you run:
```
docker-compose build
```
## And
```
docker-compose up -d
```
## 4. Work in data_ingestion_local.py
```
from airflow import DAG 
from datetime import datetime

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator



local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval = "0 6 2 * *",
    start_date = datetime(2021,1,1)
)

with local_workflow:
    wget_task = BashOperator(
        task_id = 'wget',
        bash_command = 'echo "Hello World"'

    )
    ingest_task = BashOperator(
        task_id = 'ingest',
        bash_command = 'pwd'

    )

    wget_task >> ingest_task
```
## 5. Run the workflow in localhost:8080 (Trigger the DAG in the browser)
## 6. Dome stuffs in Airflow, then create ingest_script.py to create a Python Operator
## 7. Configurate Dockerfile to connect the two docker compose.
```
Add network: airflow in Services (docker compose that has PostgreSQL connection)
```
```
Add networks:
  airflow:
    external:
      name: airflow_default in Airflow (docker compose that has PostgreSQL connection)
```
## 8. Run the docker compose that has PostgreSQL connection
```
docker-compose up -d
```
## 9. Test if all is working
```
 pgcli -h localhost -p 5432 -U root -d ny_taxi
```
## 10. Test the db in airflow
```Run docker ps to see the worker container id and then run docker exec -it <container_id> bash
```
## 11. Type Python and then import sqlachemy libray
```
import sqlalchemy
```
## 12. Create a connection to the database
```
engine = sqlalchemy.create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```
## 13. Create a connection to the database
```
engine.connect()
```
## 14. If all is working, then run all the code in ingest from the airflow UI
```
## 15. End of the tutorial
```