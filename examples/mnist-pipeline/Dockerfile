FROM python:3.7

# supervisord setup
RUN apt-get update && apt-get install -y supervisor && apt-get install -y python3-setuptools
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Airflow setup
ENV AIRFLOW_HOME=/Users/sushantikerani/airflow

RUN pip install apache-airflow
COPY /output/mnist-pipeline/main.py $AIRFLOW_HOME/dags/

RUN airflow db init

EXPOSE 8080
CMD ["/usr/bin/supervisord"]