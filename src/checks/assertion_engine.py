
from pathlib import Path
import yaml

from src.checks.null_check import check_not_null
from src.checks.unique_check import check_unique_key
from src.checks.cross_tenant_check import check_cross_tenant
from src.checks.row_count_check import check_row_count


def run_assertions(tables, config_dir):
    """
    Run YAML-defined quality checks against supplied tables.

    tables: dictionary of {table_name: pandas DataFrame}
    config_dir: path to the project's root configs directory
    """
    config_dir = Path(config_dir)
    results = []

    for config_file in sorted(config_dir.glob("*.yml")):
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        table_name = config["table"]

        if table_name not in tables:
            raise ValueError(f"Table not loaded: {table_name}")

        df = tables[table_name]

        for rule in config["checks"]:
            check_type = rule["type"]
            severity = rule["severity"].upper()

            if severity not in {"ERROR", "WARNING"}:
                raise ValueError(f"Invalid severity in {config_file.name}")

            if check_type == "not_null":
                result = check_not_null(df, rule["column"])

            elif check_type == "unique_key":
                result = check_unique_key(df, rule["columns"])

            elif check_type == "cross_tenant":
                parent_table = rule["parent_table"]

                if parent_table not in tables:
                    raise ValueError(f"Parent table not loaded: {parent_table}")

                result = check_cross_tenant(
                    child_df=df,
                    parent_df=tables[parent_table],
                    child_key=rule["child_key"],
                    parent_key=rule["parent_key"],
                    child_tenant_column=rule["child_tenant_column"],
                    parent_tenant_column=rule["parent_tenant_column"]
                )

            elif check_type == "row_count":
                result = check_row_count(
                    df,
                    rule["expected_count"]
                )

            else:
                raise ValueError(f"Unsupported check type: {check_type}")

            results.append({
                "table": table_name,
                "check": check_type,
                "severity": severity,
                "failed": result["failed"],
                "failure_count": result["failure_count"]
            })

    error_failures = sum(
        1 for item in results
        if item["failed"] and item["severity"] == "ERROR"
    )

    warning_failures = sum(
        1 for item in results
        if item["failed"] and item["severity"] == "WARNING"
    )

    pipeline_status = "HALTED" if error_failures else "PASSED"

    return {
        "pipeline_status": pipeline_status,
        "total_checks": len(results),
        "passed_checks": sum(not item["failed"] for item in results),
        "failed_checks": sum(item["failed"] for item in results),
        "error_failures": error_failures,
        "warning_failures": warning_failures,
        "results": results
    }


def print_summary(report):
    """Print counts and check metadata only; never print source records."""
    print("\n===== DATA QUALITY SUMMARY =====")
    print(f"Pipeline status: {report['pipeline_status']}")
    print(f"Total checks: {report['total_checks']}")
    print(f"Passed checks: {report['passed_checks']}")
    print(f"Failed checks: {report['failed_checks']}")
    print(f"ERROR failures: {report['error_failures']}")
    print(f"WARNING failures: {report['warning_failures']}")

    print("\n===== CHECK RESULTS =====")
    for item in report["results"]:
        status = "FAIL" if item["failed"] else "PASS"
        print(
            f"{item['table']} | {item['check']} | "
            f"{item['severity']} | {status} | "
            f"failures={item['failure_count']}"
        )