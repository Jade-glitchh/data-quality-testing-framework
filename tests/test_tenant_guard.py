
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.checks.cross_tenant_check import check_cross_tenant

clean_dir = ROOT / "data" / "clean"
corrupted_dir = ROOT / "data" / "corrupted"


def load_tables(folder):
    return {
        file.stem: pd.read_csv(file)
        for file in folder.glob("*.csv")
    }


def test_clean_accounts_have_no_tenant_violations():
    tables = load_tables(clean_dir)

    result = check_cross_tenant(
        tables["accounts"],
        tables["customers"],
        "customer_id",
        "customer_id",
        "organisation_id",
        "organisation_id"
    )

    assert result["cross_tenant_count"] == 0
    assert result["orphan_count"] == 0


def test_corrupted_accounts_detect_cross_tenant_reference():
    tables = load_tables(corrupted_dir)

    result = check_cross_tenant(
        tables["accounts"],
        tables["customers"],
        "customer_id",
        "customer_id",
        "organisation_id",
        "organisation_id"
    )

    assert result["cross_tenant_count"] == 1
    assert result["orphan_count"] == 0


if __name__ == "__main__":
    test_clean_accounts_have_no_tenant_violations()
    test_corrupted_accounts_detect_cross_tenant_reference()
    print("Tenant guard tests passed.")
