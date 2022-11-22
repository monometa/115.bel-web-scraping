import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import (
    LocalFilesystemToS3Operator,
)
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from pathlib import Path
from pyspark.sql import SparkSession

default_args = {
    "owner": "Airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    # 'retry_delay': timedelta(minutes=5),
}

# //////////////////////////////// PythonOperator - works successfully 

# def transform_spark():

#     path = Path(".")
#     path_resources = path / "resources"
#     spark = SparkSession.builder.appName("bel").getOrCreate()

#     raw_json_dataframe = (
#         spark.read.format("json")
#         .option("inferSchema", "true")
#         .load("/usr/local/spark/resources/July.json")
#     )

#     raw_json_dataframe.printSchema()

#     (raw_json_dataframe.write.options(header="True", delimiter=",")
#         .csv(f"{path_resources}/test_csv.csv")
#     )

# with DAG(
#     dag_id="spark_airflow_dag",
#     default_args=default_args,
#     # schedule_interval=None,
#     schedule_interval="@once",
#     # dagrun_timeout=timedelta(minutes=60),
#     description="use case of sparkoperator in airflow",
#     # start_date = datetime(2022, 1, 1)
# ) as dag:
#     extract = PythonOperator(
#         task_id="elt_documento_pagar_spark", python_callable=transform_spark
#     )

# (extract)

# ////////////////////////////////

# //////////////////////////////// SparkSubmitOperator - fails

with DAG(
    dag_id="spark_airflow_dag",
    default_args=default_args,
    schedule_interval="@once",
) as dag:

    transform_2_csv = SparkSubmitOperator(
        application="/usr/local/spark/app/transform_2_csv.py",
        conn_id="SparkLocal",
        task_id="spark_submit_task",
    )
(transform_2_csv)

# ////////////////////////////////