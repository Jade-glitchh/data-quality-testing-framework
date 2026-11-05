def check_unique_key(df, columns):
    duplicate_count = int(df.duplicated(subset=columns).sum())

    return {
        "check": "unique_key",
        "columns": columns,
        "failed": duplicate_count > 0,
        "failure_count": duplicate_count
    }