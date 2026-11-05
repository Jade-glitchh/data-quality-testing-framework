
from pathlib import Path
import sys
import yaml
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.checks.assertion_engine import run_assertions


def load_tables(dataset):
    folder = ROOT / "data" / dataset
    return {
        file.stem: pd.read_csv(file)
        for file in folder.glob("*.csv")
    }


def test_clean_dataset_passes():
    report = run_assertions(
        load_tables("clean"),
        ROOT / "configs"
    )

    assert report["pipeline_status"] == "PASSED"
    assert report["failed_checks"] == 0


def test_corrupted_dataset_is_halted():
    report = run_assertions(
        load_tables("corrupted"),
        ROOT / "configs"
    )

    assert report["pipeline_status"] == "HALTED"
    assert report["error_failures"] > 0


def test_warning_does_not_halt_pipeline(tmp_path):
    config = {
        "table": "customers",
        "checks": [
            {
                "type": "not_null",
                "column": "organisation_id",
                "severity": "WARNING"
            }
        ]
    }

    config_file = tmp_path / "customers.yml"

    with open(config_file, "w", encoding="utf-8") as file:
        yaml.safe_dump(config, file)

    tables = load_tables("corrupted")

    report = run_assertions(tables, tmp_path)

    assert report["pipeline_status"] == "PASSED"
    assert report["warning_failures"] == 1
    assert report["error_failures"] == 0
