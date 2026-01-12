from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(dag_id="exchange_rates_pipeline", start_date=datetime(2024, 1, 1), schedule_interval=None,   # manual trigger
         catchup=False) as dag:

    bronze = DockerOperator(
        task_id="bronze_task",
        image="pipeline_project_2-etl_worker", # container image name, could be checked with command docker images
        api_version="auto",
        auto_remove="success",
        command="python scripts/bronze_task.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="pipeline_project_2_default", # docker network, could be checked with command docker network ls
        working_dir="/app",
        mount_tmp_dir=False,
    )

    silver = DockerOperator(
        task_id="silver_task",
        image="pipeline_project_2-etl_worker",
        api_version="auto",
        auto_remove="success",
        command="python scripts/silver_task.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="pipeline_project_2_default",
        working_dir="/app",
        mount_tmp_dir=False,
    )

    bronze >> silver