from airflow import DAG
from datetime import datetime
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id="s3_etl_pipeline",
    start_date=datetime(2024, 12, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    wait_for_file = S3KeySensor(
        task_id='wait_for_amazon_s3_files',
        bucket_name='phil-ecommerce-bucket',
        bucket_key='new_files/new_TV_Final.csv',
        aws_conn_id='aws_s3',
        poke_interval=10,
        timeout=600,
    )

    load_to_snowflake = SnowflakeOperator(
        task_id='load_to_snowflake',
        snowflake_conn_id='snowflake_default',
        sql="""
        COPY INTO E_COMMERCE_DB.E_COMMERCE_SCHEMA.T_TV_DATASET
        FROM @E_COMMERCE_STAGE_S3/new_files/
        FILE_FORMAT = E_COMMERCE_DB.E_COMMERCE_SCHEMA.E_COMMERCE_CSV_FILE_FORMAT;
        """,
    )

    process_data = BashOperator(
        task_id="dbt_process_data",
        bash_command="cd /usr/local/airflow && source dbt_venv/bin/activate && dbt run --project-dir /usr/local/airflow/dbt_sales_data_processing --profiles-dir ~/.dbt"
    )

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> wait_for_file >> load_to_snowflake >> process_data >> end
