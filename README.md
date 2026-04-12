![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

# Data Engineering Project – Environment Setup (Phase 1)

## Overview
This repository contains the **Phase 1 setup** for a data engineering project focused on building a
**reproducible, production‑ready development environment** using modern data stack tools.

The goal of this phase is to eliminate local setup friction and enable rapid development using
containerized tooling and cloud‑based environments.

---

## Tech Stack
- **Python** 3.11
- **GitHub Codespaces**
- **Docker / Dev Containers**
- **PostgreSQL**
- **Apache Airflow**
- **dbt (Postgres adapter)**
- **DuckDB**
- **Pandas**

---

## Environment Setup
The project uses a `.devcontainer` configuration to ensure a consistent developer experience.

### Features
- Preconfigured Python 3.11 environment
- Automated dependency installation via `postCreateCommand`
- Ready‑to‑use PostgreSQL connectivity
- Designed for scalability and team collaboration

---

## Database Setup
- **Database:** `tpch`
- **Schemas:**
  - `raw` – source‑aligned data
  - `staging` – cleaned and transformed intermediates
  - `mart` – analytics‑ready data models

---

## Getting Started
1. Open the repository in **GitHub Codespaces**
2. The environment and dependencies initialize automatically
3. Verify PostgreSQL access:
   ```bash
   psql -U postgres

---

Versioning

Current tag: v0.1‑env‑ready
This tag represents a fully validated environment baseline


What’s Next (Phase 2)

Data ingestion pipelines
Airflow DAGs
dbt transformation models
Analytics‑ready marts


Author
Rakesh Kumar
Senior Data Engineer | Building in Public 🚀
