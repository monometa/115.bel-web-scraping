import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.hooks.S3_hook import S3Hook
# from airflow.hooks.S3_hook import S3Hook
from airflow.models.connection import Connection


def upload_to_s3(filename: str, key: str, bucket_name: str) -> None:
    hook = S3Hook('s3_connect')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)


with DAG(
    dag_id='s3_dag',
    schedule_interval='@daily',
    start_date=datetime(2021, 1, 1),
    catchup=False
) as dag:

    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        op_kwargs={
            'filename': './districts/January_2020.csv',
            'key': 'jan.csv',
            'bucket_name': '115bel'
        }
    )

    (
        task_upload_to_s3
     )
