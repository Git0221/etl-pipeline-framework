from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'rakesh',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def check_source():
    import psycopg2
    conn=psycopg2.connect( host="localhost", port=5432, database="tpch", user="postgres", password="postgres")
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM source.orders;")
    count=cursor.fetchone()[0]
    if count == 0:
        raise ValueError("Source table is empty - aborting pipeline.")
    print(f"Source table has {count} records.")
    cursor.close()
    conn.close()

def extract_to_raw():
    import psycopg2

    tables = [
        'customer',
        'lineitem',
        'nation',
        'orders',
        'part',
        'partsupp',
        'region',
        'supplier',
    ]

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="tpch",
        user="postgres",
        password="postgres",
    )
    cursor = conn.cursor()

    for table in tables:
        raw_table = f"raw.{table}"
        source_table = f"source.{table}"
        create_sql = f"""
            CREATE TABLE IF NOT EXISTS {raw_table} AS
            SELECT * FROM {source_table};
        """
        truncate_sql = f"TRUNCATE TABLE {raw_table};"

        cursor.execute(truncate_sql)
        cursor.execute(create_sql)
        print(f"Copied table {source_table} to {raw_table}.")

    conn.commit()
    cursor.close()
    conn.close()


def log_pipeline_run():
    import psycopg2

    tables = [
        'customer',
        'lineitem',
        'nation',
        'orders',
        'part',
        'partsupp',
        'region',
        'supplier',
    ]

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="tpch",
        user="postgres",
        password="postgres",
    )
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pipeline_audit (
            id SERIAL PRIMARY KEY,
            run_date TIMESTAMP NOT NULL,
            status TEXT NOT NULL,
            rows_loaded BIGINT NOT NULL
        );
        """
    )

    rows_loaded = 0
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM raw.{table};")
        rows_loaded += cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO pipeline_audit (run_date, status, rows_loaded) VALUES (%s, %s, %s);",
        (datetime.now(), 'SUCCESS', rows_loaded),
    )

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id='tpch_pipeline',
    default_args=default_args,
    description='TPC-H ETL Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 6, 1),
    catchup=False,
    tags=['tpch', 'etl']
) as dag:
    check_source_task = PythonOperator(
        task_id='check_source',
        python_callable=check_source,
    )

    extract_to_raw_task = PythonOperator(
        task_id='extract_to_raw',
        python_callable=extract_to_raw,
    )

    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command='cd /workspaces/etl-pipeline-framework/dbt && dbt run',
    )

    dbt_test_task = BashOperator(
        task_id='dbt_test',
        bash_command='cd /workspaces/etl-pipeline-framework/dbt && dbt test',
    )

    log_pipeline_run_task = PythonOperator(
        task_id='log_pipeline_run',
        python_callable=log_pipeline_run,
    )

    check_source_task >> extract_to_raw_task >> dbt_run_task >> dbt_test_task >> log_pipeline_run_task



