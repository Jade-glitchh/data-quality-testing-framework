# Data Quality Testing Framework

## 1. Project Overview

The Data Quality Testing Framework is a Python-based
framework designed to identify and report data quality
issues in relational datasets.

It uses YAML configuration files to define validation
rules and automatically execute data quality checks.

## 2. Project Objectives

- Generate synthetic datasets across 10+ relational tables.
- Define data quality rules using YAML.
- Detect missing values.
- Identify duplicate business keys.
- Detect cross-tenant data inconsistencies.
- Generate data quality reports.
- Stop pipeline execution when critical errors occur.
- Support database-independent validation logic.

## 3. Technology Stack

- Python
- Pandas
- NumPy
- PyYAML
- Pytest
- ClickHouse (planned integration)

## 4. Project Structure

- data/: Stores raw and generated datasets.
- configs/: Contains YAML validation configurations.
- src/: Contains the framework's application code.
- tests/: Contains automated tests.
- scripts/: Contains utility scripts.
- reports/: Stores validation reports.
- docs/: Contains project documentation.
- notebooks/: Contains exploratory notebooks.

## 5. Planned Data Quality Checks

- Not-null validation
- Unique-key validation
- Range validation
- Cross-tenant validation
- Row-count reconciliation

## 6. Project Status

Phase 1: Development environment setup.
Phase 2: Synthetic data generation.