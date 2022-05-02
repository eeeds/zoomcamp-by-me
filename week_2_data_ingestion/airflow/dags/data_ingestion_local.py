from airflow import DAG 
from datetime import datetime
import os 

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script  import ingest_callable

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", '/opt/airflow/')


PG_HOST=os.getenv('PG_HOST')
PG_USER=os.getenv('PG_USER')
PG_PASSWORD=os.getenv('PG_PASSWORD')
PG_PORT=os.getenv('PG_PORT')
PG_DATABASE=os.getenv('PG_DATABASE')


def download_transfer_dag(
    dag,
    url_template,
    output_file_template,
    table_name_template):

    with dag:
        wget_task = BashOperator(
            task_id = 'wget',
            bash_command = f'curl -sSLf {url_template} > {output_file_template}'

        )
        ingest_task = PythonOperator(
            task_id = 'ingest',
            python_callable = ingest_callable,
            op_kwargs = dict(
                user=PG_USER,
                password=PG_PASSWORD,
                port=PG_PORT,
                host=PG_HOST,
                db=PG_DATABASE,
                table_name=table_name_template,
                csv_file=output_file_template
            ),

        )

        wget_task >> ingest_task

#For Yellow data
yellow_data_dag = DAG(
    "LocalIngestionDagForYellowData",
    schedule_interval = "0 6 2 * *",
    start_date = datetime(2021,1,1),
    catchup = True, 
    max_active_runs= 3
)

YELLOW_URL_PREFIX = 'https://s3.amazonaws.com/nyc-tlc/trip+data/'
YELLOW_URL_TEMPLATE = YELLOW_URL_PREFIX + 'yellow_tripdata_{{ execution_date.strftime(\"%Y-%m\") }}.csv'
YELLOW_OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/yellow_taxi_{{ execution_date.strftime(\"%Y-%m\") }}.csv'
YELLOW_TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\"%Y-%m\") }}'

download_transfer_dag(
    dag = yellow_data_dag,
    url_template = YELLOW_URL_TEMPLATE,
    output_file_template = YELLOW_OUTPUT_FILE_TEMPLATE,
    table_name_template = YELLOW_TABLE_NAME_TEMPLATE
    )


#For FHV data
fhv_data_dag = DAG(
    "LocalIngestionDagForFhvData",
    schedule_interval = "0 8 2 * *",
    start_date = datetime(2019,1,1),
    end_date=datetime(2020, 1, 1),
    catchup = True,
    max_active_runs= 3
)


FHV_URL_PREFIX = 'https://nyc-tlc.s3.amazonaws.com/trip+data/'
FHV_URL_TEMPLATE = FHV_URL_PREFIX + 'fhv_tripdata_{{ execution_date.strftime(\"%Y-%m\") }}.csv'
FHV_OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/fhv_{{ execution_date.strftime(\"%Y-%m\") }}.csv'
FHV_TABLE_NAME_TEMPLATE = 'fhv_taxi_{{ execution_date.strftime(\"%Y-%m\") }}'

download_transfer_dag(
    dag = fhv_data_dag,
    url_template = FHV_URL_TEMPLATE,
    output_file_template = FHV_OUTPUT_FILE_TEMPLATE,
    table_name_template = FHV_TABLE_NAME_TEMPLATE
)


