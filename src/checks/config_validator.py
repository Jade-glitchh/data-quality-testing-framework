import yaml
from pathlib import Path

ALLOWED_TYPES = {"not_null", "unique_key", "cross_tenant", "row_count"}
ALLOWED_SEVERITIES = {"ERROR", "WARNING"}

def validate_config(file_path):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    assert isinstance(config, dict), "Configuration must be a dictionary"
    assert config.get("table"), "Missing table name"
    assert isinstance(config.get("checks"), list), "Checks must be a list"

    for check in config["checks"]:
        assert check.get("type") in ALLOWED_TYPES, "Invalid check type"
        assert check.get("severity") in ALLOWED_SEVERITIES, "Invalid severity"

        if check["type"] == "not_null":
            assert check.get("column"), "Missing column"

        elif check["type"] == "unique_key":
            assert check.get("columns"), "Missing columns"

        elif check["type"] == "row_count":
            assert isinstance(check.get("expected_count"), int), \
                "Row count requires an integer expected_count"

        elif check["type"] == "cross_tenant":
            required = [
                "parent_table",
                "child_key",
                "parent_key",
                "child_tenant_column",
                "parent_tenant_column"
            ]
            for field in required:
                assert check.get(field), f"Missing {field}"

    return config["table"]


if __name__ == "__main__":
    config_files = sorted(Path("configs").glob("*.yml"))

    for file in config_files:
        print(f"Checking: {file.name}")

        try:
            table_name = validate_config(file)
            print(f"{table_name}: VALID")

        except Exception as error:
            print(f"{file.name}: FAILED - {error}")