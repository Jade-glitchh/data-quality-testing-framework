# Data Quality Framework – System Architecture

## 1. Architecture Overview

The framework uses a modular, configuration-driven architecture. It separates synthetic data generation, validation rules, execution logic, database integration and reporting.

## 2. Data Flow

```text
       Synthetic Data
       (10 CSV Tables)
              |
              v
       Dataset Selection
        Clean / Corrupted
              |
              v
       YAML Configuration
       (49 Quality Checks)
              |
              v
       Python Validation Functions
       - Not Null
       - Unique Key
       - Cross Tenant
       - Row Count
              |
              v
       Central Assertion Engine
              |
              v
       Severity Evaluation
         /          \
        /            \
     ERROR          WARNING
       |                |
       v                v
    HALTED            CONTINUE
       \                /
        \              /
         v            v
         Quality Reporting
          CSV and JSON
              |
              v
         Reports Folder
```

## 3. Main Components

### Data Layer
Contains clean and intentionally corrupted synthetic CSV datasets across 10 relational tables.

### Configuration Layer
Contains one YAML configuration per table. Each configuration defines the applicable checks, expected values and severity levels.

### Validation Layer
Contains reusable Python functions responsible for executing individual data quality checks.

### Assertion Engine
Loads configurations, selects the relevant checks, executes them and determines the overall pipeline status.

### Database Integration
Docker Compose starts ClickHouse. The demonstration script loads CSV tables into ClickHouse, retrieves them and passes the resulting DataFrames to the assertion engine.

### Reporting Layer
Exports quality results as CSV and JSON, including check status, severity, failure counts and pipeline status.

### Automation Layer
GitHub Actions automatically validates YAML configurations and executes the automated test suite when changes are pushed or pull requests are opened against `main`.

## 4. Design Considerations

- **Modularity:** Individual checks can be maintained and extended independently.
- **Reusability:** YAML configurations allow validation rules to be reused across tables.
- **Database independence:** Core validation functions operate on Pandas DataFrames rather than directly executing ClickHouse-specific SQL.
- **Tenant isolation:** Cross-tenant checks help prevent invalid relationships between organisations.
- **Privacy:** Quality reports contain aggregate failure information rather than raw customer records.
- **Reliability:** ERROR-level failures halt the pipeline, while WARNING-level failures are reported without stopping execution.

## 5. Execution Entry Points

Local execution:

```bash
python scripts/run_quality_engine.py clean
python scripts/run_quality_engine.py corrupted
```

Docker and ClickHouse execution:

```bash
docker compose run --rm quality-runner clean
docker compose run --rm quality-runner corrupted
```

Automated testing:

```bash
pytest -v
```