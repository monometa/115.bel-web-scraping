
FROM apache/airflow:latest

ARG SPARK_VERSION="3.1.2"
ARG HADOOP_VERSION="3.2"

USER root

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR $AIRFLOW_HOME

# JAVA installation
# Java is required in order to spark-submit work
# Install OpenJDK-11
RUN apt update && \
    apt-get install wget unzip zip -y && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# AWS CLI installation:
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip 
RUN sudo ./aws/install 

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# Spark installation
ENV SPARK_HOME /usr/local/spark

RUN cd "/tmp" && \
        wget --no-verbose "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
        tar -xvzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
        mkdir -p "${SPARK_HOME}/bin" && \
        mkdir -p "${SPARK_HOME}/assembly/target/scala-2.12/jars" && \
        cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/." "${SPARK_HOME}/bin/" && \
        cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/." "${SPARK_HOME}/assembly/target/scala-2.12/jars/" && \
        rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

RUN export SPARK_HOME
ENV PATH $PATH:/usr/local/spark/bin

# download extra modules for linux
# git gcc g++ -qqq
ENV PATH="/root/.local/bin/:$PATH"
COPY requirements.txt .

RUN chmod -R 777 /opt/airflow/*
USER $AIRFLOW_UID
RUN pip install --no-cache-dir -r requirements.txt