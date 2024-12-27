from airflow import DAG
from datetime import datetime
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

with DAG(
    dag_id="s3_etl_pipeline",
    start_date=datetime(2024, 12, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    wait_for_file = S3KeySensor(
        task_id='wait_for_s3_file_pattern',
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

    # run_dbt = BashOperator(
    #     task_id='run_dbt_models',
    #     bash_command='dbt run --project-dir /path/to/dbt/project --profiles-dir /path/to/profiles',
    # )

    wait_for_file >> load_to_snowflake
