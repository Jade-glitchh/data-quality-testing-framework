from pathlib import Path
import sys
import pandas as pd

# Add the project root to Python's import path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.checks.null_check import check_not_null
from src.checks.unique_check import check_unique_key
from src.checks.cross_tenant_check import check_cross_tenant
from src.checks.row_count_check import check_row_count

clean_dir = ROOT / "data" / "clean"
corrupted_dir = ROOT / "data" / "corrupted"

# Load the test datasets
clean_customers = pd.read_csv(clean_dir / "customers.csv")
corrupt_customers = pd.read_csv(corrupted_dir / "customers.csv")

clean_accounts = pd.read_csv(clean_dir / "accounts.csv")
corrupt_accounts = pd.read_csv(corrupted_dir / "accounts.csv")


print("\n--- CLEAN DATA TESTS ---")

print(check_not_null(clean_customers, "organisation_id"))

print(check_unique_key(
    clean_customers,
    ["organisation_id", "customer_id"]
))

print(check_cross_tenant(
    clean_accounts,
    clean_customers,
    "customer_id",
    "customer_id",
    "organisation_id",
    "organisation_id"
))

print(check_row_count(clean_customers, len(clean_customers)))


print("\n--- CORRUPTED DATA TESTS ---")

print(check_not_null(corrupt_customers, "organisation_id"))

print(check_unique_key(
    corrupt_customers,
    ["organisation_id", "customer_id"]
))

print(check_cross_tenant(
    corrupt_accounts,
    corrupt_customers,
    "customer_id",
    "customer_id",
    "organisation_id",
    "organisation_id"
))

print(check_row_count(corrupt_customers, len(clean_customers)))