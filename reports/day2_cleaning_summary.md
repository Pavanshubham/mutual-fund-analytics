# Day 2 Cleaning Summary

## Cleaning tasks completed
- Parsed all relevant date columns into datetime format
- Sorted NAV history by `amfi_code` and `date`
- Removed duplicate rows from all datasets
- Validated NAV values to ensure NAV > 0
- Forward-filled NAV within each AMFI code where needed
- Standardized investor transaction types into:
  - SIP
  - LUMPSUM
  - REDEMPTION
- Validated investor transaction amounts > 0
- Standardized KYC status values and flagged invalid enum values
- Validated numeric performance columns in scheme_performance
- Flagged expense ratio anomalies outside 0.1% to 2.5%
- Saved all cleaned datasets into `data/processed/`
- Loaded cleaned data into SQLite database

## Outputs generated
- 10 cleaned CSV files in `data/processed/`
- `bluestock_mf.db`
- `sql/schema.sql`
- `sql/queries.sql`
- `reports/data_dictionary.md`
- `reports/day2_cleaning_summary.csv`