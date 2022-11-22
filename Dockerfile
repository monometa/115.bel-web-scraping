
FROM apache/airflow:2.4.3

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////// FIRST VERSION 

# ARG SPARK_VERSION="3.1.2"
# ARG HADOOP_VERSION="3.2"

# USER root

# ENV AIRFLOW_HOME=/opt/airflow
# ENV SPARK_HOME=/usr/local/spark
# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

# WORKDIR $AIRFLOW_HOME

# # JAVA installation
# # Java is required in order to spark-submit work
# # Install OpenJDK-11
# RUN apt update && \
#     apt-get install wget unzip zip -y && \
#     apt-get install -y openjdk-11-jdk && \
#     apt-get install -y ant && \
#     apt-get clean;

# RUN export JAVA_HOME

# # AWS CLI installation:
# RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# RUN unzip awscliv2.zip 
# RUN sudo ./aws/install 

# # Spark installation

# RUN cd "/tmp" && \
#         wget --no-verbose "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
#         tar -xvzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
#         mkdir -p "${SPARK_HOME}/bin" && \
#         mkdir -p "${SPARK_HOME}/assembly/target/scala-2.12/jars" && \
#         cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/." "${SPARK_HOME}/bin/" && \
#         cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/." "${SPARK_HOME}/assembly/target/scala-2.12/jars/" && \
#         rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

# RUN export SPARK_HOME
# ENV PATH $PATH:/usr/local/spark/bin

# ENV PATH="/root/.local/bin/:$PATH"
# COPY requirements.txt .

# RUN chmod -R 777 /opt/airflow/*
# USER $AIRFLOW_UID
# RUN pip install --no-cache-dir -r requirements.txt

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Install Python requirements
USER root
SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

# Install Java
RUN apt update && \
    mkdir -pv /usr/share/man/man1 \
    && mkdir -pv /usr/share/man/man7 \
    && curl -fsSL https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - \
    && echo 'deb https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ buster main' > \
    /etc/apt/sources.list.d/adoptopenjdk.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    adoptopenjdk-8-hotspot-jre \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/adoptopenjdk-8-hotspot-jre-amd64

# Install Spark
ENV SPARK_HOME=/spark-3.0.1-bin-hadoop3.2
ENV HADOOP_HOME=$SPARK_HOME
ENV HADOOP_CONF_DIR=$SPARK_HOME/conf

RUN curl -O https://archive.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz \
    && tar -C / -zxvf ./spark-3.0.1-bin-hadoop3.2.tgz
USER $AIRFLOW_UID
COPY requirements.txt .
RUN pip install -r requirements.txt
