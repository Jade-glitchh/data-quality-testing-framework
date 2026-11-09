
from pathlib import Path
import os
import sys
import json
import re

import pandas as pd
import clickhouse_connect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def connect_to_clickhouse():
    return clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST", "localhost"),
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "")
    )


def clickhouse_type(series):
    if pd.api.types.is_bool_dtype(series):
        return "Nullable(UInt8)"
    elif pd.api.types.is_integer_dtype(series):
        return "Nullable(Int64)"
    elif pd.api.types.is_float_dtype(series):
        return "Nullable(Float64)"
    else:
        return "Nullable(String)"


def load_tables(client, dataset):
    data_dir = ROOT / "data" / dataset
    database = "quality_demo"

    client.command(f"CREATE DATABASE IF NOT EXISTS {database}")

    csv_files = sorted(data_dir.glob("*.csv"))

    if len(csv_files) != 10:
        raise ValueError(
            f"Expected 10 CSV tables, found {len(csv_files)}"
        )

    for file in csv_files:
        table_name = file.stem

        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", table_name):
            raise ValueError(f"Invalid table name: {table_name}")

        df = pd.read_csv(file)

        columns = ", ".join(
            f"`{column}` {clickhouse_type(df[column])}"
            for column in df.columns
        )

        client.command(
            f"DROP TABLE IF EXISTS {database}.{table_name}"
        )

        client.command(
            f"""
            CREATE TABLE {database}.{table_name}
            ({columns})
            ENGINE = MergeTree
            ORDER BY tuple()
            """
        )

        insert_df = df.astype(object).where(pd.notna(df), None)

        if not insert_df.empty:
            client.insert_df(
                f"{database}.{table_name}",
                insert_df
            )

        print(
            f"Loaded {table_name}: {len(df)} rows"
        )

    return csv_files


def read_tables_from_clickhouse(client, csv_files):
    database = "quality_demo"
    tables = {}

    for file in csv_files:
        table_name = file.stem

        tables[table_name] = client.query_df(
            f"SELECT * FROM {database}.{table_name}"
        )

    return tables


def main():
    dataset = sys.argv[1] if len(sys.argv) > 1 else "clean"

    if dataset not in {"clean", "corrupted"}:
        raise ValueError("Choose either clean or corrupted")

    client = connect_to_clickhouse()

    try:
        print("\nConnected to ClickHouse.")

        csv_files = load_tables(client, dataset)

        print("\nReading tables back from ClickHouse.")

        tables = read_tables_from_clickhouse(
            client,
            csv_files
        )

        from src.checks.assertion_engine import (
            run_assertions,
            print_summary
        )

        report = run_assertions(
            tables=tables,
            config_dir=ROOT / "configs"
        )

        print_summary(report)

        report_dir = ROOT / "reports"
        report_dir.mkdir(exist_ok=True)

        pd.DataFrame(report["results"]).to_csv(
            report_dir / f"clickhouse_{dataset}_report.csv",
            index=False
        )

        with open(
            report_dir / f"clickhouse_{dataset}_report.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(report, file, indent=4)

        print("\nClickHouse quality reports saved.")

        return 1 if report["pipeline_status"] == "HALTED" else 0

    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
