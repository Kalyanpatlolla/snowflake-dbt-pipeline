from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    "owner": "kalyan",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="snowflake_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 5, 18),
    schedule=None,
    catchup=False,
) as dag:

    # Task 1: Run dbt models
    dbt_run = BashOperator(
        task_id="run_dbt_models",
        bash_command="""
        cd /workspaces/snowflake-dbt-pipeline/snowflake_dbt_project &&
        dbt run
        """
    )

    # Task 2: Test dbt models
    dbt_test = BashOperator(
        task_id="test_dbt_models",
        bash_command="""
        cd /workspaces/snowflake-dbt-pipeline/snowflake_dbt_project &&
        dbt test
        """
    )

    # Task 3: Generate dbt docs
    dbt_docs = BashOperator(
        task_id="generate_dbt_docs",
        bash_command="""
        cd /workspaces/snowflake-dbt-pipeline/snowflake_dbt_project &&
        dbt docs generate
        """
    )

    # Define task order
    dbt_run >> dbt_test >> dbt_docs

