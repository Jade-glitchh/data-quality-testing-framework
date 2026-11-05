
from pathlib import Path
import yaml

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"

EXPECTED_COUNTS = {
    "organisations": 3,
    "customers": 15,
    "accounts": 30,
    "advisors": 9,
    "portfolios": 30,
    "securities": 10,
    "holdings": 90,
    "transactions": 150,
    "trades": 180,
    "fee_schedules": 9
}

for file_path in CONFIG_DIR.glob("*.yml"):
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    table_name = config["table"]

    if not any(
        rule["type"] == "row_count"
        for rule in config["checks"]
    ):
        config["checks"].append({
            "type": "row_count",
            "expected_count": EXPECTED_COUNTS[table_name],
            "severity": "ERROR"
        })

    with open(file_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(config, file, sort_keys=False)

    print(f"Updated: {table_name}")

print("Row-count rules added.")