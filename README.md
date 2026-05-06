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
├── airflow/
│   └── dags/
│       └── tpch_pipeline.py     # Main Airflow DAG
│
├── dbt/
│   ├── dbt_project.yml
│   ├── packages.yml
│   └── models/
│       ├── raw/                 # Bronze layer
│       ├── staging/             # Silver layer
│       └── mart/                # Gold layer
│
├── scripts/
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

### 5. Verify data loaded

```bash
psql -U postgres -d tpch -c "SELECT COUNT(*) FROM source.orders;"
# Expected: 150,000 rows at sf=0.1
```

---

## Database Setup

The project uses four schemas inside the `tpch` database:

| Schema | Layer | Purpose |
|---|---|---|
| `source` | Operational | Raw TPC-H data loaded by seed script |
| `raw` | Bronze | Exact copy of source, no transformations |
| `staging` | Silver | Cleaned, typed, renamed columns |
| `mart` | Gold | Business metrics and aggregations |

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

- [x] Phase 1 — Environment Setup (Codespaces + Python + Postgres)
- [x] Phase 2 — Source Data (TPC-H seeded into Postgres)
- [ ] Phase 3 — Airflow DAG
- [ ] Phase 4 — dbt Models (Raw → Staging → Mart)
- [ ] Phase 5 — Data Quality Framework
- [ ] Phase 6 — Documentation & Runbook

---

## Versioning

| Tag | Description |
|---|---|
| `v0.1-env-ready` | Environment fully validated |
| `v0.2-data-seeded` | TPC-H data loaded into Postgres |

---

## Author

**Rakesh Kumar**  
Senior Database Engineer 
Azure Data Factory · SQL Server · Snowflake · Python

*Building in public — follow the commits to see the project evolve.*
