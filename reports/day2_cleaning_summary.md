# Day 2 Cleaning Summary – Mutual Fund Analytics Project

## Objective

The objective of Day 2 was to clean the raw mutual fund datasets, validate important business rules, standardize key fields, and load cleaned data into a structured SQLite star schema for analysis.

---

# Cleaning Tasks Completed

## 1. `01_fund_master.csv`

* Trimmed leading/trailing spaces from text columns
* Converted `launch_date` to datetime format
* Removed duplicate rows

## 2. `02_nav_history.csv`

* Parsed `date` column to datetime
* Sorted records by `amfi_code` and `date`
* Removed duplicate records
* Validated that `nav > 0`
* Forward-filled missing NAV values within each AMFI code where required

## 3. `03_aum_by_fund_house.csv`

* Converted `date` to datetime
* Removed duplicates

## 4. `04_monthly_sip_inflows.csv`

* Converted `month` to datetime
* Preserved null values in `yoy_growth_pct` where prior-year comparison was unavailable
* Removed duplicates

## 5. `05_category_inflows.csv`

* Converted `month` to datetime
* Removed duplicates

## 6. `06_industry_folio_count.csv`

* Converted `month` to datetime
* Removed duplicates

## 7. `07_scheme_performance.csv`

* Standardized text fields
* Converted return and risk metric columns to numeric
* Validated return columns for numeric consistency
* Flagged expense ratio anomalies outside the expected range of **0.1% to 2.5%**
* Removed duplicates

## 8. `08_investor_transactions.csv`

* Standardized transaction types into:

  * `SIP`
  * `LUMPSUM`
  * `REDEMPTION`
* Parsed `transaction_date` to datetime
* Validated `amount_inr > 0`
* Standardized KYC status values
* Flagged invalid KYC status enum values
* Removed duplicates

## 9. `09_portfolio_holdings.csv`

* Converted `portfolio_date` to datetime
* Removed duplicates

## 10. `10_benchmark_indices.csv`

* Converted `date` to datetime
* Removed duplicates

---

# Data Quality Checks Performed

The following business and technical validations were performed:

* Date parsing and datetime standardization
* Duplicate removal across all datasets
* NAV validation (`nav > 0`)
* Transaction amount validation (`amount_inr > 0`)
* KYC status standardization and flagging
* Expense ratio anomaly flagging in performance data
* Numeric conversion of return and performance metrics
* Text standardization / trimming of string columns

---

# Outputs Generated

## Cleaned CSVs

Saved in:

```text
data/processed/
```

Files generated:

* `01_fund_master_cleaned.csv`
* `02_nav_history_cleaned.csv`
* `03_aum_by_fund_house_cleaned.csv`
* `04_monthly_sip_inflows_cleaned.csv`
* `05_category_inflows_cleaned.csv`
* `06_industry_folio_count_cleaned.csv`
* `07_scheme_performance_cleaned.csv`
* `08_investor_transactions_cleaned.csv`
* `09_portfolio_holdings_cleaned.csv`
* `10_benchmark_indices_cleaned.csv`

## Reports Generated

Saved in:

```text
reports/
```

Files generated:

* `day2_cleaning_summary.csv`
* `day2_cleaning_summary.md`
* `data_dictionary.md`

## SQLite Database

Created:

* `bluestock_mf.db`

## SQL Files

Saved in:

```text
sql/
```

Files generated:

* `schema.sql`
* `queries.sql`

---

# SQLite Star Schema Created

The following analytical star schema tables were created in SQLite:

### Dimension Tables

* `dim_fund`
* `dim_date`

### Fact Tables

* `fact_nav`
* `fact_transactions`
* `fact_performance`
* `fact_aum`

---

# Result

Day 2 successfully completed the **data cleaning, anomaly handling, schema design, and SQLite loading pipeline**. The project is now ready for **Day 3 exploratory data analysis (EDA), SQL analytics, and dashboard-focused insights generation**.
