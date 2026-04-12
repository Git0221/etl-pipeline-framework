# Scripts

## seed_data.py

Generates TPC-H benchmark data using DuckDB and loads all 8 tables into the postgres 'source' schema

## Prerequisites
- Postgers running on localhost:5432
- Database 'tpch' exist with 'source' schema
- Python packages: duckdb, psycopg2-binary,pandas

## Usage

# Default (sf=0.1)
python scripts/seed_data.py

# Custom scale factor
python scripts/seed_data.py --scale-factor 0.1

## Expected Output as sf=0.1

| Table    | Rows    |
-----------|---------|
| orders   | 150,000 |
| lineitem | 600,572 |
| customer | 15,000  |
| nation   | 25      |
| region   | 5       |
| part     | 20,000  |
| partsupp | 80,000  |
| supplier | 1,000   |