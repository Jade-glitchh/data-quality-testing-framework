def check_not_null(df, column):
    missing_count = int(df[column].isna().sum())

    return {
        "check": "not_null",
        "column": column,
        "failed": missing_count > 0,
        "failure_count": missing_count
    }