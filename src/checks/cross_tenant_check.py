
def check_cross_tenant(
    child_df,
    parent_df,
    child_key,
    parent_key,
    child_tenant_column,
    parent_tenant_column
):
    parent_keys = set(parent_df[parent_key].dropna())

    parent_pairs = set(
        zip(
            parent_df[parent_key],
            parent_df[parent_tenant_column]
        )
    )

    cross_tenant_count = 0
    orphan_count = 0

    for key, tenant in zip(
        child_df[child_key],
        child_df[child_tenant_column]
    ):
        if key not in parent_keys:
            orphan_count += 1

        elif (key, tenant) not in parent_pairs:
            cross_tenant_count += 1

    failure_count = cross_tenant_count + orphan_count

    return {
        "check": "cross_tenant",
        "failed": failure_count > 0,
        "failure_count": failure_count,
        "cross_tenant_count": cross_tenant_count,
        "orphan_count": orphan_count
    }