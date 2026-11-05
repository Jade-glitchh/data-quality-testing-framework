
# Data Quality Remediation Runbooks

## 1. Missing Required Values

**Check:** `not_null`

**Severity:** ERROR

**Meaning:** A required column contains missing values.

**Example:** A customer record has no organisation_id.

**Remediation:**
1. Identify the affected table and column from the quality report.
2. Trace the source data or ingestion process.
3. Confirm the correct value from an authorised source.
4. Correct the source record or transformation logic.
5. Rerun the quality checks.

**Pipeline action:** Halt when severity is ERROR.

---

## 2. Duplicate Records

**Check:** `unique_key`

**Severity:** ERROR

**Meaning:** A key that should uniquely identify a record appears more than once.

**Example:** Two customers share the same organisation_id and customer_id.

**Remediation:**
1. Review the affected table and key definition.
2. Identify the source of duplication.
3. Determine which record is valid.
4. Correct the upstream process or deduplication logic.
5. Rerun the quality checks.

**Pipeline action:** Halt when severity is ERROR.

---

## 3. Cross-Tenant Reference Violations

**Check:** `cross_tenant`

**Severity:** ERROR

**Meaning:** A child record references a parent record belonging to a different organisation, or the parent reference does not exist.

**Remediation:**
1. Identify the affected child and parent tables.
2. Check the tenant identifiers used in the relationship.
3. Confirm that both records belong to the same organisation.
4. Correct the relationship or reject the invalid record.
5. Rerun the tenant guard checks.

**Security note:** Never bypass tenant isolation to make a check pass.

**Pipeline action:** Halt when severity is ERROR.

---

## 4. Row Count Mismatch

**Check:** `row_count`

**Severity:** ERROR

**Meaning:** The actual number of records differs from the expected baseline.

**Remediation:**
1. Compare expected and actual record counts.
2. Check source extraction and ingestion logs.
3. Investigate missing, duplicated, or unexpectedly added records.
4. Correct the extraction or loading process.
5. Update the expected baseline only when an authorised data change explains the difference.
6. Rerun the checks.

**Pipeline action:** Halt when severity is ERROR.

---

## 5. WARNING-Level Failures

**Meaning:** A quality issue has been detected but is not configured to block the pipeline.

**Remediation:**
1. Review the affected table and check.
2. Assess the impact of the issue.
3. Record the investigation and corrective action.
4. Escalate to ERROR severity if the issue presents a critical data or security risk.

**Pipeline action:** Log and report the warning; continue execution.

---

## Logging and Data Privacy

- Reports contain table names, check types, severity, status, and failure counts.
- Do not print raw customer records or sensitive personal information.
- Restrict access to detailed reports according to organisational policy.
