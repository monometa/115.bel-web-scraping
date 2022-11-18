import os
from pyspark.sql import SparkSession


# aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
# aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

spark = SparkSession.builder.appName('bel').getOrCreate()

# hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.s3a.access.key", aws_access_key)
# hadoop_conf.set("fs.s3a.secret.key", aws_secret_key)
# hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

raw_json_dataframe = spark.read.format("json") \
                            .option("inferSchema","true") \
                            .load("/usr/local/spark/resources/July.json")

raw_json_dataframe.printSchema()
# raw_json_dataframe.createOrReplaceTempView("Mutual_benefit")

# raw_json_dataframe.format('csv').option('header','true').save('mycsv.csv',mode='overwrite')

# spark-submit --master spark://172.20.0.10:7077 scripts/transform_2_parquet.py