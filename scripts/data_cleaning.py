import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

cleaning_log = []

def log_step(dataset, before_rows, after_rows, notes):
    cleaning_log.append({
        "dataset": dataset,
        "before_rows": before_rows,
        "after_rows": after_rows,
        "rows_removed": before_rows - after_rows,
        "notes": notes
    })

def save_df(df, filename):
    output_path = os.path.join(PROCESSED_PATH, filename)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path} | Shape: {df.shape}")


# =========================================================
# 1. fund_master
# =========================================================
fund_master = pd.read_csv(f"{RAW_PATH}/01_fund_master.csv")
before = len(fund_master)

for col in fund_master.select_dtypes(include="object").columns:
    fund_master[col] = fund_master[col].astype(str).str.strip()

fund_master["launch_date"] = pd.to_datetime(fund_master["launch_date"], errors="coerce")
fund_master = fund_master.drop_duplicates()

after = len(fund_master)
log_step("01_fund_master", before, after, "Stripped text columns, converted launch_date to datetime, removed duplicates.")
save_df(fund_master, "01_fund_master_cleaned.csv")


# =========================================================
# 2. nav_history
# =========================================================
nav_history = pd.read_csv(f"{RAW_PATH}/02_nav_history.csv")
before = len(nav_history)

nav_history["date"] = pd.to_datetime(nav_history["date"], errors="coerce")
nav_history = nav_history.sort_values(["amfi_code", "date"])
nav_history = nav_history.drop_duplicates()

# Keep only NAV > 0
nav_history = nav_history[nav_history["nav"] > 0]

# Forward fill missing NAV per scheme
nav_history["nav"] = nav_history.groupby("amfi_code")["nav"].ffill()

after = len(nav_history)
log_step("02_nav_history", before, after, "Parsed dates, sorted by amfi_code/date, removed duplicates, validated NAV > 0, forward-filled NAV within each amfi_code.")
save_df(nav_history, "02_nav_history_cleaned.csv")


# =========================================================
# 3. aum_by_fund_house
# =========================================================
aum = pd.read_csv(f"{RAW_PATH}/03_aum_by_fund_house.csv")
before = len(aum)

aum["date"] = pd.to_datetime(aum["date"], errors="coerce")
aum = aum.drop_duplicates()

after = len(aum)
log_step("03_aum_by_fund_house", before, after, "Converted date to datetime and removed duplicates.")
save_df(aum, "03_aum_by_fund_house_cleaned.csv")


# =========================================================
# 4. monthly_sip_inflows
# =========================================================
sip = pd.read_csv(f"{RAW_PATH}/04_monthly_sip_inflows.csv")
before = len(sip)

sip["month"] = pd.to_datetime(sip["month"], format="%Y-%m", errors="coerce")
sip = sip.drop_duplicates()

after = len(sip)
log_step("04_monthly_sip_inflows", before, after, "Converted month to datetime. Kept YoY null values because early months may not have prior-year base.")
save_df(sip, "04_monthly_sip_inflows_cleaned.csv")


# =========================================================
# 5. category_inflows
# =========================================================
category_inflows = pd.read_csv(f"{RAW_PATH}/05_category_inflows.csv")
before = len(category_inflows)

category_inflows["month"] = pd.to_datetime(category_inflows["month"], format="%Y-%m", errors="coerce")
category_inflows = category_inflows.drop_duplicates()

after = len(category_inflows)
log_step("05_category_inflows", before, after, "Converted month to datetime and removed duplicates.")
save_df(category_inflows, "05_category_inflows_cleaned.csv")


# =========================================================
# 6. industry_folio_count
# =========================================================
folio = pd.read_csv(f"{RAW_PATH}/06_industry_folio_count.csv")
before = len(folio)

folio["month"] = pd.to_datetime(folio["month"], format="%Y-%m", errors="coerce")
folio = folio.drop_duplicates()

after = len(folio)
log_step("06_industry_folio_count", before, after, "Converted month to datetime and removed duplicates.")
save_df(folio, "06_industry_folio_count_cleaned.csv")


# =========================================================
# 7. scheme_performance
# =========================================================
performance = pd.read_csv(f"{RAW_PATH}/07_scheme_performance.csv")
before = len(performance)

for col in performance.select_dtypes(include="object").columns:
    performance[col] = performance[col].astype(str).str.strip()

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

performance = performance.drop_duplicates()

after = len(performance)
log_step("07_scheme_performance", before, after, "Validated numeric return fields, flagged expense_ratio outside 0.1%–2.5%, removed duplicates.")
save_df(performance, "07_scheme_performance_cleaned.csv")


# =========================================================
# 8. investor_transactions
# =========================================================
txn = pd.read_csv(f"{RAW_PATH}/08_investor_transactions.csv")
before = len(txn)

txn["transaction_type"] = txn["transaction_type"].astype(str).str.strip().str.upper()

txn["transaction_type"] = txn["transaction_type"].replace({
    "SIP": "SIP",
    "SYSTEMATIC INVESTMENT PLAN": "SIP",
    "LUMPSUM": "LUMPSUM",
    "LUMP SUM": "LUMPSUM",
    "REDEMPTION": "REDEMPTION",
    "SELL": "REDEMPTION"
})

txn["transaction_date"] = pd.to_datetime(txn["transaction_date"], errors="coerce")

txn = txn[txn["amount_inr"] > 0]

txn["kyc_status"] = txn["kyc_status"].astype(str).str.strip().str.title()

valid_kyc = ["Verified", "Pending", "Rejected"]
txn["kyc_flag"] = np.where(txn["kyc_status"].isin(valid_kyc), "OK", "FLAG")

txn = txn.drop_duplicates()

after = len(txn)
log_step("08_investor_transactions", before, after, "Standardized transaction_type, validated amount > 0, parsed dates, checked KYC enum values, removed duplicates.")
save_df(txn, "08_investor_transactions_cleaned.csv")


# =========================================================
# 9. portfolio_holdings
# =========================================================
holdings = pd.read_csv(f"{RAW_PATH}/09_portfolio_holdings.csv")
before = len(holdings)

holdings["portfolio_date"] = pd.to_datetime(holdings["portfolio_date"], errors="coerce")
holdings = holdings.drop_duplicates()

after = len(holdings)
log_step("09_portfolio_holdings", before, after, "Converted portfolio_date to datetime and removed duplicates.")
save_df(holdings, "09_portfolio_holdings_cleaned.csv")


# =========================================================
# 10. benchmark_indices
# =========================================================
benchmark = pd.read_csv(f"{RAW_PATH}/10_benchmark_indices.csv")
before = len(benchmark)

benchmark["date"] = pd.to_datetime(benchmark["date"], errors="coerce")
benchmark = benchmark.drop_duplicates()

after = len(benchmark)
log_step("10_benchmark_indices", before, after, "Converted date to datetime and removed duplicates.")
save_df(benchmark, "10_benchmark_indices_cleaned.csv")


# =========================================================
# Save cleaning summary
# =========================================================
summary_df = pd.DataFrame(cleaning_log)
summary_df.to_csv("reports/day2_cleaning_summary.csv", index=False)

print("\nAll datasets cleaned successfully.")
print("Cleaning summary saved to reports/day2_cleaning_summary.csv")