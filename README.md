![Python](https://img.shields.io/badge/Python-3.11-blue)
![Airflow](https://img.shields.io/badge/Airflow-2.9.2-green)
![dbt](https://img.shields.io/badge/dbt-1.11-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

# ETL Pipeline Framework

A production-grade data pipeline built with Apache Airflow, dbt, and PostgreSQL — demonstrating medallion architecture, SCD Type 2 handling, data quality frameworks, and full orchestration on a real-world benchmark dataset (TPC-H).

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Git0221/etl-pipeline-framework)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEDALLION ARCHITECTURE                      │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  SOURCE  │    │   RAW    │    │ STAGING  │    │   MART   │  │
│  │          │───▶│ (Bronze) │───▶│ (Silver) │───▶│  (Gold)  │  │
│  │ TPC-H    │    │ exact    │    │ cleaned  │    │ business │  │
│  │ DuckDB   │    │ copy     │    │ typed    │    │ metrics  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Airflow DAG ──▶ dbt run ──▶ dbt test ──▶ Quality Check │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## What This Project Demonstrates

- **Medallion Architecture** — Bronze / Silver / Gold layered data model
- **Apache Airflow** — Production DAG with retries, SLA callbacks, and failure logging
- **dbt** — Staging models, mart models, SCD Type 2 on customer dimension
- **Data Quality Framework** — Row count thresholds, null rates, freshness checks
- **Pipeline Audit Logging** — Every run logged to `pipeline_audit` table with status and row counts
- **TPC-H Benchmark Dataset** — Industry-standard schema with realistic business queries
- **GitHub Codespaces** — Zero-install development environment, runs in the browser
- **psycopg2 COPY** — High-performance bulk loading into PostgreSQL

---

## Project Structure

```
etl-pipeline-framework/
│
├── .devcontainer/
│   └── devcontainer.json        # Codespaces environment definition
│
├── airflow/                     ✅ Complete
│   └── dags/
│       └── tpch_pipeline.py     # Main Airflow DAG — 5 tasks
│
├── dbt/                         🔜 In Progress
│   ├── dbt_project.yml
│   ├── packages.yml
│   └── models/
│       ├── raw/                 # Bronze layer
│       ├── staging/             # Silver layer
│       └── mart/                # Gold layer
│
├── scripts/                     ✅ Complete
│   ├── seed_data.py             # TPC-H → Postgres loader
│   ├── data_quality.py          # Post-load quality checks
│   └── README.md                # Scripts documentation
│
├── docs/
│   ├── ARCHITECTURE.md          # Detailed architecture decisions
│   └── RUNBOOK.md               # Operational runbook
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Airflow DAG — tpch_pipeline

The DAG runs daily and consists of 5 tasks in sequence:

```
check_source → extract_to_raw → dbt_run → dbt_test → log_pipeline_run
```

| Task | Type | Description |
|---|---|---|
| `check_source` | PythonOperator | Validates source tables exist and have rows |
| `extract_to_raw` | PythonOperator | Copies all 8 tables from `source` to `raw` schema |
| `dbt_run` | BashOperator | Runs all dbt models (raw → staging → mart) |
| `dbt_test` | BashOperator | Runs all dbt data quality tests |
| `log_pipeline_run` | PythonOperator | Logs run status and row counts to `pipeline_audit` |

**Production-grade features:**
- `retries: 2` with 5-minute retry delay on all tasks
- `pipeline_audit` table captures every run — date, status, total rows loaded
- `catchup=False` prevents backfill on first run
- `TRUNCATE` before reload prevents duplicate data in raw layer

---

## Getting Started

### 1. Open in GitHub Codespaces

Click the **Open in GitHub Codespaces** button above. The environment
builds automatically — Python 3.11, PostgreSQL 15, Airflow, and dbt
are all installed via `devcontainer.json`. No local setup required.

### 2. Verify the environment

```bash
python --version        # 3.11.x
airflow version         # 2.9.2
dbt --version           # 1.11.x
psql -U postgres -c "SELECT version();"
```

### 3. Set up the database

```bash
psql -U postgres -c "CREATE DATABASE tpch;"
psql -U postgres -d tpch -c "CREATE SCHEMA source;"
psql -U postgres -d tpch -c "CREATE SCHEMA raw;"
psql -U postgres -d tpch -c "CREATE SCHEMA staging;"
psql -U postgres -d tpch -c "CREATE SCHEMA mart;"
```

### 4. Seed the source data

```bash
# Default scale factor (sf=0.1, ~100MB)
python scripts/seed_data.py

# Larger dataset (sf=1, ~1GB — needs 4GB+ RAM)
python scripts/seed_data.py --scale-factor 1
```

### 5. Start Airflow

```bash
export AIRFLOW_HOME=/workspaces/etl-pipeline-framework/airflow
airflow standalone
```

### 6. Trigger the pipeline

Open the Airflow UI on port 8080, find `tpch_pipeline` and click **Trigger DAG**.

---

## Database Setup

The project uses five schemas inside the `tpch` database:

| Schema | Layer | Purpose |
|---|---|---|
| `source` | Operational | Raw TPC-H data loaded by seed script |
| `raw` | Bronze | Exact copy of source, no transformations |
| `staging` | Silver | Cleaned, typed, renamed columns |
| `mart` | Gold | Business metrics and aggregations |
| `public` | System | Pipeline audit log table |

---

## Dataset — TPC-H

TPC-H is the industry-standard benchmark for analytical database systems.
It consists of 8 tables modelling a product supplier database:

| Table | Description | Rows (sf=0.1) |
|---|---|---|
| orders | Customer orders | 150,000 |
| lineitem | Order line items | 600,572 |
| customer | Customer dimension | 15,000 |
| supplier | Supplier dimension | 1,000 |
| part | Parts catalogue | 20,000 |
| partsupp | Part-supplier relationships | 80,000 |
| nation | Nation reference | 25 |
| region | Region reference | 5 |

---

## Current Status

- [x] Phase 1 — Environment Setup (Codespaces + Python 3.11 + PostgreSQL 15)
- [x] Phase 2 — Source Data (TPC-H seeded into Postgres via DuckDB)
- [x] Phase 3 — Airflow DAG (5 tasks + pipeline audit logging)
- [ ] Phase 4 — dbt Models (Raw → Staging → Mart + SCD Type 2)
- [ ] Phase 5 — Data Quality Framework
- [ ] Phase 6 — Documentation & Runbook

---

## Versioning

| Tag | Description |
|---|---|
| `v0.1-env-ready`   | Environment fully validated       |
| `v0.2-data-seeded` | TPC-H data loaded into Postgres   |
| `v0.3-airflow-dag` | Airflow DAG with 5 tasks complete |

---

## Author

**Rakesh Kumar**
Senior Database Engineer | 19 Years Experience
Oracle · SQL Server · Snowflake · AWS Redshift

*Building in public — follow the commits to see the project evolve.*
