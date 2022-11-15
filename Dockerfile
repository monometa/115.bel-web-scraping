
FROM apache/airflow:latest

ENV AIRFLOW_HOME=/opt/airflow

USER root
WORKDIR $AIRFLOW_HOME

RUN apt-get update -qq && apt-get install vim -qqq && apt-get install unzip

# installation AWS CLI:
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip 
RUN sudo ./aws/install

# download extra modules for linux
# git gcc g++ -qqq
ENV PATH="/root/.local/bin/:$PATH"
COPY requirements.txt .
RUN chmod -R 777 /opt/airflow/*
USER $AIRFLOW_UID
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
