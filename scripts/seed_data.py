import argparse
import duckdb
import pandas as pd
import psycopg2
from io import StringIO

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate TPC-H data in DuckDB and load it into PostgreSQL"
    )

    parser.add_argument(
        "--scale-factor",
        "--sf",
        type=float,
        default=0.1,
        help="TPC-H scale factor (e.g. 0.1, 1, 10). Default: 0.1"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    scale_factor = args.scale_factor

    # Connect to DuckDB
    con = duckdb.connect()

    print(f"Generating TPC-H data with scale factor: {scale_factor}")
    con.execute(f"CALL dbgen(sf={scale_factor})")

    tables = con.execute("SHOW TABLES").fetchall()
    print("Tables generated:", tables)

    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "tpch"

    try:
        pg_conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = pg_conn.cursor()

        for table in tables:
            table_name = table[0]
            print(f"Processing table: {table_name}")

            # Fetch data from DuckDB
            df = con.execute(f"SELECT * FROM {table_name}").fetchdf()

            # Create table DDL (all TEXT as per your original design)
            cols = ", ".join([f'"{c}" TEXT' for c in df.columns])

            cursor.execute(f"DROP TABLE IF EXISTS source.{table_name}")
            cursor.execute(f"CREATE TABLE source.{table_name} ({cols})")

            # Bulk load using COPY
            buffer = StringIO()
            df.to_csv(buffer, index=False, header=False)
            buffer.seek(0)

            cursor.copy_expert(
                f"COPY source.{table_name} FROM STDIN WITH CSV",
                buffer
            )

            pg_conn.commit()
            print(f"Table {table_name} loaded successfully.")

        cursor.close()
        pg_conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()