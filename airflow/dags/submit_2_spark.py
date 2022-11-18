import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
# from airflow.hooks.S3_hook import S3Hook
from airflow.models.connection import Connection
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
}

spark_dag = DAG(
        dag_id = "spark_airflow_dag",
        default_args=default_args,
        # schedule_interval=None,	
        schedule_interval="@once",
        # dagrun_timeout=timedelta(minutes=60),
        description='use case of sparkoperator in airflow',
        # start_date = datetime(2022, 1, 1)
        )
Extract = SparkSubmitOperator(
		application ='./scripts/tranform_2_parquet.py',
		conn_id= 'SparkLocal', 
		task_id='spark_submit_task', 
		dag=spark_dag
		)
Extract