# Day 1 - Data Ingestion Anomalies Report

## Project

Mutual Fund Analytics Platform

## Date

24 June 2026

---

# Dataset Summary

A total of 10 datasets were successfully loaded and inspected.

| Dataset                  | Rows   | Columns | Missing Values |
| ------------------------ | ------ | ------- | -------------- |
| 01_fund_master           | 40     | 15      | 0              |
| 02_nav_history           | 46,000 | 3       | 0              |
| 03_aum_by_fund_house     | 90     | 5       | 0              |
| 04_monthly_sip_inflows   | 48     | 6       | 12             |
| 05_category_inflows      | 144    | 3       | 0              |
| 06_industry_folio_count  | 21     | 6       | 0              |
| 07_scheme_performance    | 40     | 19      | 0              |
| 08_investor_transactions | 32,778 | 13      | 0              |
| 09_portfolio_holdings    | 322    | 8       | 0              |
| 10_benchmark_indices     | 8,050  | 3       | 0              |

---

# Identified Anomalies

## 1. Missing Values Detected

### Dataset: 04_monthly_sip_inflows.csv

Missing Values: 12

Column affected:

* yoy_growth_pct

Observation:

* The first 12 records contain NULL values for Year-over-Year Growth Percentage.
* This is expected because YoY growth cannot be calculated until at least one year of historical data is available.

Severity: Low

Recommended Action:

* Keep NULL values during ingestion.
* Handle during analysis by excluding NULL records or calculating growth where sufficient historical data exists.

---

## 2. Date Columns Stored as String

The following datasets contain date fields currently loaded as object/string datatype:

* 02_nav_history.csv
* 03_aum_by_fund_house.csv
* 04_monthly_sip_inflows.csv
* 06_industry_folio_count.csv
* 08_investor_transactions.csv
* 09_portfolio_holdings.csv
* 10_benchmark_indices.csv

Observation:

* Dates should be converted to datetime format during preprocessing.

Severity: Medium

Recommended Action:

```python
pd.to_datetime(column_name)
```

---

## 3. Categorical Columns Loaded as Object

Many categorical attributes are stored as generic object types:

Examples:

* fund_house
* category
* sub_category
* risk_category
* transaction_type
* state
* city
* gender
* payment_mode

Observation:

* These fields are suitable candidates for category datatype optimization.

Severity: Low

Recommended Action:

```python
df[col] = df[col].astype("category")
```

---

## 4. Large NAV History Dataset

Dataset:

* 02_nav_history.csv

Rows:

46,000

Observation:

* Historical NAV data represents the largest dataset in the project.
* Future joins with benchmark and transaction datasets may require indexing and query optimization.

Severity: Informational

Recommended Action:

* Load into SQL database with index on:

  * amfi_code
  * date

---

## 5. Investor Transaction Dataset Size

Dataset:

* 08_investor_transactions.csv

Rows:

32,778

Observation:

* Dataset is sufficiently large for investor behavior analysis.
* No missing values detected.

Severity: None

---

## 6. No Missing Values in Core Mutual Fund Master Data

Datasets:

* 01_fund_master.csv
* 02_nav_history.csv
* 03_aum_by_fund_house.csv
* 05_category_inflows.csv
* 06_industry_folio_count.csv
* 07_scheme_performance.csv
* 08_investor_transactions.csv
* 09_portfolio_holdings.csv
* 10_benchmark_indices.csv

Observation:

* Core datasets demonstrate excellent completeness.

Severity: None

---

# Data Quality Assessment

## Completeness

Excellent

Only 12 missing values identified across all datasets.

## Consistency

Good

Column naming conventions are consistent and AMFI scheme codes appear standardized.

## Validity

Good

Numeric columns contain appropriate numeric datatypes.
No obvious datatype violations detected.

## Uniqueness

Pending Validation

Duplicate checks and AMFI code cross-validation will be performed in Day 2.

---

# Overall Assessment

Data Quality Score: 9.5 / 10

The dataset collection is clean, well-structured, and suitable for downstream analytics, SQL warehousing, dashboard development, and machine learning workflows.

Primary action item for Day 2:

* Convert date columns to datetime format.
* Validate AMFI code relationships across datasets.
* Check duplicate records.
* Load datasets into SQL database.
