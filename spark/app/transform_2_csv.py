import os
from pathlib import Path
from pyspark.sql import SparkSession

path = Path("/opt/airflow")
path_resources = path / "resources"
spark = SparkSession.builder.appName("bel").getOrCreate()

raw_json_dataframe = (
    spark.read.format("json")
    .option("inferSchema", "true")
    .load("/usr/local/spark/resources/July.json")
)

raw_json_dataframe.printSchema()

raw_json_dataframe.write.csv(f"{path_resources}/test.csv")
# spark-submit --master spark://172.20.0.10:7077 scripts/transform_2_parquet.py
