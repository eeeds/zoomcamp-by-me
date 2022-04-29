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
## Work in data_ingestion_local.py
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
## Run the workflow in localhost:8080 (Trigger the DAG in the browser)