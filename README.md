# Data Quality & Testing Framework

A configuration-driven data quality testing framework built with Python, YAML, PostgreSQL-compatible data processing concepts, Docker and ClickHouse.

## 1. Project Overview

The Data Quality & Testing Framework is a Python-based framework designed to automatically detect, validate and report data quality issues across relational datasets.

The framework uses YAML configuration files to define validation rules and a central assertion engine to execute checks against multiple tables.

It supports automated detection of missing values, duplicate business keys, cross-tenant inconsistencies and unexpected row-count changes.

The framework also implements severity-based pipeline execution: critical errors halt pipeline execution, while warnings are recorded without stopping the pipeline.

A ClickHouse integration demonstrates how the framework can load, retrieve and validate data using a database backend.

## 2. Project Objectives

- Generate synthetic datasets across 10 normalized relational tables.
- Define data quality rules through YAML configuration files.
- Build reusable Python validation functions.
- Implement a central data quality assertion engine.
- Detect missing values and duplicate business keys.
- Identify cross-tenant data inconsistencies.
- Perform row-count reconciliation.
- Support ERROR and WARNING severity levels.
- Halt pipeline execution when critical errors are detected.
- Generate structured CSV and JSON quality reports.
- Demonstrate database integration using ClickHouse.
- Automate configuration validation and testing through GitHub Actions.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Framework development and execution |
| Pandas | Data loading and processing |
| NumPy | Synthetic data generation |
| PyYAML | YAML configuration management |
| Pytest | Automated testing |
| ClickHouse | Database integration and demonstration |
| Docker | Containerisation and reproducible execution |
| Git & GitHub | Version control and project hosting |
| GitHub Actions | Continuous integration and automated testing |

## 4. Project Architecture

The framework follows a configuration-driven validation architecture.

1. **Data generation:** Synthetic clean and corrupted datasets are generated across 10 relational tables.
2. **Configuration:** YAML files define validation rules and their severity levels.
3. **Validation engine:** Python functions execute individual quality checks.
4. **Assertion engine:** A central engine coordinates the checks and determines pipeline status.
5. **Database integration:** ClickHouse stores the demonstration tables and provides data back to the assertion engine.
6. **Reporting:** Results are exported into CSV and JSON reports.
7. **Automation:** Pytest and GitHub Actions validate the framework and its configurations.

### Architecture Flow

```text
Synthetic Datasets (10 Tables)
          |
          v
   YAML Configurations
          |
          v
   Python Quality Checks
          |
          v
   Central Assertion Engine
          |
          v
    ClickHouse Integration
          |
          v
   Severity-Based Evaluation
          |
          v
   Quality Reports (CSV/JSON)
          |
          v
   Pipeline Status
   PASS / HALT
```

## 5. Project Structure

```text
data-quality-testing-framework/
│
├── .github/
│   └── workflows/
│       └── quality-checks.yml
│
├── configs/
│   ├── accounts.yml
│   ├── advisors.yml
│   ├── customers.yml
│   ├── fee_schedules.yml
│   ├── holdings.yml
│   ├── organisations.yml
│   ├── portfolios.yml
│   ├── securities.yml
│   ├── trades.yml
│   └── transactions.yml
│
├── data/
│   ├── clean/
│   ├── corrupted/
│   ├── generated/
│   └── raw/
│
├── docs/
│   └── remediation_runbooks.md
│
├── notebooks/
│
├── reports/
│
├── scripts/
│   ├── run_quality_engine.py
│   └── run_clickhouse_demo.py
│
├── src/
│   └── checks/
│       ├── assertion_engine.py
│       ├── config_validator.py
│       ├── cross_tenant_check.py
│       ├── null_check.py
│       ├── row_count_check.py
│       └── unique_check.py
│
├── tests/
│   ├── test_assertion_engine.py
│   ├── test_quality_checks.py
│   └── test_tenant_guard.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 6. Implemented Data Quality Checks

| Check | Description |
|---|---|
| Not-null | Detects missing values in required columns |
| Unique-key | Identifies duplicate business keys |
| Cross-tenant | Detects invalid or cross-organisation references |
| Row-count | Compares actual table records against expected counts |

Validation rules are configured independently for each table using YAML.

## 7. Severity-Based Execution

The framework supports two severity levels:

**ERROR**
- Indicates a critical data quality failure.
- Causes the pipeline to halt.
- Prevents corrupted data from passing validation.

**WARNING**
- Indicates a non-critical quality issue.
- Records the failure in the report.
- Allows pipeline execution to continue.

## 8. Synthetic Dataset

The project uses a Wealth Management / Financial Services dataset containing 10 relational tables.

| Table | Clean records |
|---|---:|
| Organisations | 3 |
| Customers | 15 |
| Accounts | 30 |
| Advisors | 9 |
| Portfolios | 30 |
| Securities | 10 |
| Holdings | 90 |
| Transactions | 150 |
| Trades | 180 |
| Fee Schedules | 9 |
| **Total** | **526** |

Two dataset versions are maintained:

- **Clean dataset:** Contains the original valid records.
- **Corrupted dataset:** Contains intentionally planted data quality issues, including missing organisation IDs, duplicate customer keys and cross-tenant references.

## 9. Installation and Setup

### Prerequisites

- Python 3.13
- Git
- Docker Desktop
- Docker Compose

### Clone the repository

```bash
git clone https://github.com/Jade-glitchh/data-quality-testing-framework.git

cd data-quality-testing-framework
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows CMD:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 10. Running the Framework

### Validate YAML configurations

```bash
python src/checks/config_validator.py
```

### Run the clean dataset

```bash
python scripts/run_quality_engine.py clean
```

### Run the corrupted dataset

```bash
python scripts/run_quality_engine.py corrupted
```

### Run automated tests

```bash
pytest -v
```

## 11. Docker and ClickHouse Demonstration

The project includes a Docker-based ClickHouse integration.

Start ClickHouse:

```bash
docker compose up -d clickhouse
```

Run the clean dataset:

```bash
docker compose run --rm quality-runner clean
```

Run the corrupted dataset:

```bash
docker compose run --rm quality-runner corrupted
```

The demonstration loads the 10 CSV tables into ClickHouse, reads them back and executes the central assertion engine.

To stop the services:

```bash
docker compose down
```

## 12. Testing Results

The framework has been tested against both clean and intentionally corrupted datasets.

### Clean dataset

| Metric | Result |
|---|---:|
| Total checks | 49 |
| Passed checks | 49 |
| Failed checks | 0 |
| Pipeline status | PASSED |

### Corrupted dataset

| Metric | Result |
|---|---:|
| Total checks | 49 |
| Passed checks | 44 |
| Failed checks | 5 |
| ERROR failures | 5 |
| Pipeline status | HALTED |

The five detected failures include:

- One cross-tenant account reference.
- One account row-count mismatch.
- One missing customer organisation ID.
- One duplicate customer business key.
- One customer row-count mismatch.

### Automated tests

All five automated tests passed:

```text
5 passed
```

## 13. Reporting

The framework generates structured reports in the `reports/` directory.

Reports include:

- Clean dataset quality report (CSV and JSON).
- Corrupted dataset quality report (CSV and JSON).
- ClickHouse clean dataset report (CSV and JSON).
- ClickHouse corrupted dataset report (CSV and JSON).

The reports contain validation outcomes, severity levels, failure counts and pipeline status without exposing raw customer records.

## 14. Continuous Integration

GitHub Actions is configured to automatically:

1. Check out the repository.
2. Set up Python 3.13.
3. Install project dependencies.
4. Validate YAML configurations.
5. Execute automated tests.

The workflow runs on pushes and pull requests targeting the `main` branch.

## 15. Remediation Documentation

The `docs/remediation_runbooks.md` file provides guidance for investigating and resolving:

- Missing required values.
- Duplicate business keys.
- Cross-tenant reference violations.
- Row-count mismatches.
- Warning-level failures.

## 16. Project Status

**Status: Core implementation completed and CI workflow successfully tested.**

Implemented components:

- Synthetic data generation.
- YAML-based configuration management.
- Reusable data quality checks.
- Central assertion engine.
- Tenant guard validation.
- Severity-based pipeline execution.
- CSV and JSON reporting.
- Automated testing with Pytest.
- Docker containerisation.
- ClickHouse integration.
- GitHub Actions CI workflow.
- Remediation runbooks.

## 17. Future Improvements

Potential extensions include:

- Additional validation rules such as range and referential-integrity checks.
- Support for additional database backends.
- Scheduled data quality monitoring.
- Historical quality trend analysis.
- Alerting and notification integrations.
- More advanced pipeline observability.

## 18. Repository

GitHub: https://github.com/Jade-glitchh/data-quality-testing-framework

---

**Project:** Data Quality & Testing Framework  
**Focus:** Data Engineering, Data Quality, Automated Testing and Pipeline Reliability