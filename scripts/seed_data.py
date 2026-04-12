import duckdb
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

# Connect to the DuckDB database
con=duckdb.connect()

con.execute("CALL dbgen(sf=1)")

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
    # Create a SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Connect to the database
    with engine.connect() as connection:
        # Execute a simple query to verify the connection
        for table in tables:
            table_name = table[0]
            print(f"Copying data for table: {table_name}")
            # Read data from DuckDB
            df = con.execute(f"SELECT * FROM {table_name}").fetchdf()
            # Write data to PostgreSQL
            df.to_sql(table_name, con=con, if_exists='replace', index=False,schema='source')
            con.commit()
            print(f"Data for table {table_name} loaded successfully.")


except SQLAlchemyError as e:
    print(f"An error occurred: {e}")