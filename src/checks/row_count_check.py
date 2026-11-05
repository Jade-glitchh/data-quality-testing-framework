def check_row_count(df, expected_count):
    actual_count = len(df)

    return {
        "check": "row_count",
        "expected_count": expected_count,
        "actual_count": actual_count,
        "failed": actual_count != expected_count,
        "failure_count": abs(actual_count - expected_count)
    }