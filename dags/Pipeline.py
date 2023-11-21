from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.models import Variable
import json
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator


BUCKET_NAME = Variable.get("BUCKET")
EMR_ID = Variable.get("EMR_ID")
EMR_STEPS = {}
with open("./dags/scripts/emr/run_emr.json") as json_file:
    EMR_STEPS = json.load(json_file)

default_args = {
    'owner': 'airflow',
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime(2023, 11, 7),
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
        dag_id='us_immigration_pipeline',
        default_args=default_args,
        description='data pipeline for us immigration data warehouse'

) as dag:

    landing_to_work = S3CopyObjectOperator(
        task_id='landing_to_work',
        source_bucket_key="landing/",
        dest_bucket_key='work/',
        aws_conn_id='aws_default',
        source_bucket_name=BUCKET_NAME,
        dest_bucket_name=BUCKET_NAME
    )

    transform_data = EmrAddStepsOperator(
        dag=dag,
        task_id="transform_data",
        job_flow_id=EMR_ID,
        aws_conn_id="aws_default",
        steps=EMR_STEPS,
        params={
            "BUCKET_NAME": BUCKET_NAME,
            "staging": "work",
            "production": "production"
        },
        depends_on_past=True,
    )

    generate_staging_table = PostgresOperator(
        dag=dag,
        task_id="generate_staging_table",
        sql="scripts/sql/generate_staging_table.sql",
        postgres_conn_id="redshift",
    )

    load_to_datawarehouse = PostgresOperator(
        dag=dag,
        task_id="load_to_datawarehouse",
        sql="scripts/sql/load_to_datawarehouse.sql",
        postgres_conn_id="redshift",
    )

    landing_to_work >> transform_data >> generate_staging_table >> load_to_datawarehouse
