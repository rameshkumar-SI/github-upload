from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime,timedelta
import boto3
s3 = boto3.resource('s3')

def upload_file_to_s3(filename,key,bucket_name):
    s3.bucket(bucket_name).upload_file(filenmae,key)


default_args = {
    'owner':'airflow',
    'start_date':datetime(2021,2,15),
    'retry_delay':timedelta(minutes=5)
}

# set the context manager
with DAG('s3_dag_test',default_args=default_args,schedule_interval='@once') as dag:
    
    start_task = DummyOperator(
        task_id = "dummary_start"
    )

    upload_to_s3_task = PythonOperator(
        task_id = 'upload_file_to_s3',
        python_callable = lambda _:print("uploading file to S3")
    )
# set dependencies
start_task >> upload_to_s3_task