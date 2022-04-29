from airflow import DAG 
from datetime import datetime
import os 

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", '/opt/airflow/')

local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval = "0 6 2 * *",
    start_date = datetime(2021,1,1)
)

URL_PREFIX = 'https://s3.amazonaws.com/nyc-tlc/trip+data/'
URL_TEMPLATE = URL_PREFIX + 'yellow_tripdata_2021-01.csv'
with local_workflow:
    wget_task = BashOperator(
        task_id = 'wget',
        #bash_command = f'curl -sS {url} > {AIRFLOW_HOME}/output.csv'
        bash_command = 'echo "{{ ds }}" "{{ execution_date.strftime(\"%Y-%m\") }}"'

    )
    ingest_task = BashOperator(
        task_id = 'ingest',
        bash_command = f'ls {AIRFLOW_HOME}'

    )

    wget_task >> ingest_task