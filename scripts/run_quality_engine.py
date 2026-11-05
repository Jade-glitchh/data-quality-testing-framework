
from pathlib import Path
import sys
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.checks.assertion_engine import run_assertions, print_summary


def main():
    dataset = sys.argv[1] if len(sys.argv) > 1 else "clean"

    if dataset not in {"clean", "corrupted"}:
        raise ValueError("Choose either 'clean' or 'corrupted'")

    data_dir = ROOT / "data" / dataset
    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)

    tables = {
        file.stem: pd.read_csv(file)
        for file in data_dir.glob("*.csv")
    }

    print(f"Loaded {len(tables)} tables from {dataset} dataset.")

    report = run_assertions(
        tables=tables,
        config_dir=ROOT / "configs"
    )

    print_summary(report)

    # Save detailed check results as CSV
    results_df = pd.DataFrame(report["results"])
    results_df.to_csv(
        report_dir / f"{dataset}_quality_report.csv",
        index=False
    )

    # Save summary and check results as JSON
    with open(
        report_dir / f"{dataset}_quality_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4)

    print(f"\nReports saved in: {report_dir}")

    return 1 if report["pipeline_status"] == "HALTED" else 0


if __name__ == "__main__":
    sys.exit(main())
