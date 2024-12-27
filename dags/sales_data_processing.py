from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dbt_sales_workflow",
    start_date=datetime(2024, 12, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /usr/local/airflow && source dbt_venv/bin/activate && dbt run --project-dir /usr/local/airflow/dbt_sales_data_processing --profiles-dir ~/.dbt"
    )   

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /usr/local/airflow && source dbt_venv/bin/activate dbt test --project-dir /usr/local/airflow/dbt_sales_data_processing --profiles-dir ~/.dbt"
    )

    dbt_run >> dbt_test
