import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"
REPORTS_PATH = "reports"

os.makedirs(PROCESSED_PATH, exist_ok=True)
os.makedirs(REPORTS_PATH, exist_ok=True)

cleaning_log = []

def log_step(dataset, before_rows, after_rows, duplicates_removed, null_counts_before, null_counts_after, notes):
    cleaning_log.append({
        "dataset": dataset,
        "before_rows": before_rows,
        "after_rows": after_rows,
        "rows_removed": before_rows - after_rows,
        "duplicates_removed": duplicates_removed,
        "nulls_before": int(null_counts_before),
        "nulls_after": int(null_counts_after),
        "notes": notes
    })

def save_df(df, filename):
    output_path = os.path.join(PROCESSED_PATH, filename)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path} | Shape: {df.shape}")

def strip_text_columns(df):
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
    return df

print("=" * 80)
print("DAY 2 - DATA CLEANING PIPELINE STARTED")
print("=" * 80)

# =========================================================
# 1. fund_master
# =========================================================
fund_master = pd.read_csv(f"{RAW_PATH}/01_fund_master.csv")
before = len(fund_master)
null_before = fund_master.isna().sum().sum()

fund_master = strip_text_columns(fund_master)
fund_master["launch_date"] = pd.to_datetime(fund_master["launch_date"], errors="coerce")

dup_before = len(fund_master)
fund_master = fund_master.drop_duplicates()
duplicates_removed = dup_before - len(fund_master)

null_after = fund_master.isna().sum().sum()
after = len(fund_master)

log_step(
    "01_fund_master",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Trimmed text fields, converted launch_date to datetime, removed duplicates."
)
save_df(fund_master, "01_fund_master_cleaned.csv")


# =========================================================
# 2. nav_history
# =========================================================
nav_history = pd.read_csv(f"{RAW_PATH}/02_nav_history.csv")
before = len(nav_history)
null_before = nav_history.isna().sum().sum()

nav_history["date"] = pd.to_datetime(nav_history["date"], errors="coerce")
nav_history = nav_history.sort_values(["amfi_code", "date"])

dup_before = len(nav_history)
nav_history = nav_history.drop_duplicates()
duplicates_removed = dup_before - len(nav_history)

# Keep only valid NAV values
nav_history = nav_history[nav_history["nav"] > 0]

# Forward fill NAV within each fund
nav_history["nav"] = nav_history.groupby("amfi_code")["nav"].ffill()

null_after = nav_history.isna().sum().sum()
after = len(nav_history)

log_step(
    "02_nav_history",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Parsed date, sorted by amfi_code/date, removed duplicates, validated NAV > 0, forward-filled NAV within each AMFI code."
)
save_df(nav_history, "02_nav_history_cleaned.csv")


# =========================================================
# 3. aum_by_fund_house
# =========================================================
aum = pd.read_csv(f"{RAW_PATH}/03_aum_by_fund_house.csv")
before = len(aum)
null_before = aum.isna().sum().sum()

aum = strip_text_columns(aum)
aum["date"] = pd.to_datetime(aum["date"], errors="coerce")

dup_before = len(aum)
aum = aum.drop_duplicates()
duplicates_removed = dup_before - len(aum)

null_after = aum.isna().sum().sum()
after = len(aum)

log_step(
    "03_aum_by_fund_house",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Converted date to datetime and removed duplicates."
)
save_df(aum, "03_aum_by_fund_house_cleaned.csv")


# =========================================================
# 4. monthly_sip_inflows
# =========================================================
sip = pd.read_csv(f"{RAW_PATH}/04_monthly_sip_inflows.csv")
before = len(sip)
null_before = sip.isna().sum().sum()

sip["month"] = pd.to_datetime(sip["month"], format="%Y-%m", errors="coerce")

dup_before = len(sip)
sip = sip.drop_duplicates()
duplicates_removed = dup_before - len(sip)

null_after = sip.isna().sum().sum()
after = len(sip)

log_step(
    "04_monthly_sip_inflows",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Converted month to datetime. YoY growth nulls retained where prior-year comparison was unavailable."
)
save_df(sip, "04_monthly_sip_inflows_cleaned.csv")


# =========================================================
# 5. category_inflows
# =========================================================
category_inflows = pd.read_csv(f"{RAW_PATH}/05_category_inflows.csv")
before = len(category_inflows)
null_before = category_inflows.isna().sum().sum()

category_inflows = strip_text_columns(category_inflows)
category_inflows["month"] = pd.to_datetime(category_inflows["month"], format="%Y-%m", errors="coerce")

dup_before = len(category_inflows)
category_inflows = category_inflows.drop_duplicates()
duplicates_removed = dup_before - len(category_inflows)

null_after = category_inflows.isna().sum().sum()
after = len(category_inflows)

log_step(
    "05_category_inflows",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Converted month to datetime and removed duplicates."
)
save_df(category_inflows, "05_category_inflows_cleaned.csv")


# =========================================================
# 6. industry_folio_count
# =========================================================
folio = pd.read_csv(f"{RAW_PATH}/06_industry_folio_count.csv")
before = len(folio)
null_before = folio.isna().sum().sum()

folio["month"] = pd.to_datetime(folio["month"], format="%Y-%m", errors="coerce")

dup_before = len(folio)
folio = folio.drop_duplicates()
duplicates_removed = dup_before - len(folio)

null_after = folio.isna().sum().sum()
after = len(folio)

log_step(
    "06_industry_folio_count",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Converted month to datetime and removed duplicates."
)
save_df(folio, "06_industry_folio_count_cleaned.csv")


# =========================================================
# 7. scheme_performance
# =========================================================
performance = pd.read_csv(f"{RAW_PATH}/07_scheme_performance.csv")
before = len(performance)
null_before = performance.isna().sum().sum()

performance = strip_text_columns(performance)

numeric_cols = [
    "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
    "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
    "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
    "aum_crore", "expense_ratio_pct", "morningstar_rating"
]

for col in numeric_cols:
    performance[col] = pd.to_numeric(performance[col], errors="coerce")

performance["expense_ratio_flag"] = np.where(
    (performance["expense_ratio_pct"] < 0.1) | (performance["expense_ratio_pct"] > 2.5),
    "FLAG",
    "OK"
)

dup_before = len(performance)
performance = performance.drop_duplicates()
duplicates_removed = dup_before - len(performance)

null_after = performance.isna().sum().sum()
after = len(performance)

log_step(
    "07_scheme_performance",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Validated numeric return fields, converted metrics to numeric, flagged expense ratio anomalies outside 0.1%–2.5%, removed duplicates."
)
save_df(performance, "07_scheme_performance_cleaned.csv")


# =========================================================
# 8. investor_transactions
# =========================================================
txn = pd.read_csv(f"{RAW_PATH}/08_investor_transactions.csv")
before = len(txn)
null_before = txn.isna().sum().sum()

txn = strip_text_columns(txn)

txn["transaction_type"] = txn["transaction_type"].str.upper().replace({
    "SIP": "SIP",
    "SYSTEMATIC INVESTMENT PLAN": "SIP",
    "LUMPSUM": "LUMPSUM",
    "LUMP SUM": "LUMPSUM",
    "REDEMPTION": "REDEMPTION",
    "SELL": "REDEMPTION"
})

txn["transaction_date"] = pd.to_datetime(txn["transaction_date"], errors="coerce")

# Keep only valid transaction amounts
txn = txn[txn["amount_inr"] > 0]

txn["kyc_status"] = txn["kyc_status"].str.title()
valid_kyc = ["Verified", "Pending", "Rejected"]
txn["kyc_flag"] = np.where(txn["kyc_status"].isin(valid_kyc), "OK", "FLAG")

dup_before = len(txn)
txn = txn.drop_duplicates()
duplicates_removed = dup_before - len(txn)

null_after = txn.isna().sum().sum()
after = len(txn)

log_step(
    "08_investor_transactions",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Standardized transaction types, validated amount > 0, parsed transaction dates, standardized KYC values, flagged invalid KYC enum values, removed duplicates."
)
save_df(txn, "08_investor_transactions_cleaned.csv")


# =========================================================
# 9. portfolio_holdings
# =========================================================
holdings = pd.read_csv(f"{RAW_PATH}/09_portfolio_holdings.csv")
before = len(holdings)
null_before = holdings.isna().sum().sum()

holdings = strip_text_columns(holdings)
holdings["portfolio_date"] = pd.to_datetime(holdings["portfolio_date"], errors="coerce")

dup_before = len(holdings)
holdings = holdings.drop_duplicates()
duplicates_removed = dup_before - len(holdings)

null_after = holdings.isna().sum().sum()
after = len(holdings)

log_step(
    "09_portfolio_holdings",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Converted portfolio_date to datetime and removed duplicates."
)
save_df(holdings, "09_portfolio_holdings_cleaned.csv")


# =========================================================
# 10. benchmark_indices
# =========================================================
benchmark = pd.read_csv(f"{RAW_PATH}/10_benchmark_indices.csv")
before = len(benchmark)
null_before = benchmark.isna().sum().sum()

benchmark = strip_text_columns(benchmark)
benchmark["date"] = pd.to_datetime(benchmark["date"], errors="coerce")

dup_before = len(benchmark)
benchmark = benchmark.drop_duplicates()
duplicates_removed = dup_before - len(benchmark)

null_after = benchmark.isna().sum().sum()
after = len(benchmark)

log_step(
    "10_benchmark_indices",
    before,
    after,
    duplicates_removed,
    null_before,
    null_after,
    "Converted date to datetime and removed duplicates."
)
save_df(benchmark, "10_benchmark_indices_cleaned.csv")


# =========================================================
# Save cleaning summary report
# =========================================================
summary_df = pd.DataFrame(cleaning_log)
summary_csv_path = os.path.join(REPORTS_PATH, "day2_cleaning_summary.csv")
summary_df.to_csv(summary_csv_path, index=False)

print("\n" + "=" * 80)
print("DAY 2 CLEANING COMPLETED SUCCESSFULLY")
print("=" * 80)
print(summary_df.to_string(index=False))
print(f"\nCleaning summary saved to: {summary_csv_path}")