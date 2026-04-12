import duckdb
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import psycopg2
from io import StringIO

# Connect to the DuckDB database
con=duckdb.connect()

con.execute("CALL dbgen(sf=0.1)")

tables=con.execute("SHOW TABLES").fetchall()
print(tables)

DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='localhost'
DB_PORT='5432'
DB_NAME='tpch'

# Create database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    pg_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT)
    cursor = pg_conn.cursor()
    for table in tables:
        table_name = table[0]
        print(f"Processing table: {table_name}")
        
        # Fetch data from DuckDB
        df = con.execute(f"SELECT * FROM {table_name}").fetchdf()

        #Create table from dataframe
        cols=", ".join(
            [f'"{c}" TEXT' for c in df.columns]
        )
        cursor.execute(f"DROP TABLE IF EXISTS source.{table_name}")
        
        cursor.execute(f"CREATE TABLE source.{table_name} ({cols})")

        #Bulk load using copy
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        cursor.copy_expert(f"COPY source.{table_name} FROM STDIN WITH CSV", buffer)
        pg_conn.commit()
        print(f"Table {table_name} loaded successfully.")

    cursor.close()    
    pg_conn.close()
except Exception as e:
    print(f"An error occurred: {e}")

   