import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = "bluestock_mf.db"
PROCESSED_PATH = "data/processed"

engine = create_engine(f"sqlite:///{DB_PATH}")

# ============================
# Load processed datasets
# ============================
fund_master = pd.read_csv(f"{PROCESSED_PATH}/01_fund_master_cleaned.csv")
nav_history = pd.read_csv(f"{PROCESSED_PATH}/02_nav_history_cleaned.csv")
aum = pd.read_csv(f"{PROCESSED_PATH}/03_aum_by_fund_house_cleaned.csv")
sip = pd.read_csv(f"{PROCESSED_PATH}/04_monthly_sip_inflows_cleaned.csv")
category_inflows = pd.read_csv(f"{PROCESSED_PATH}/05_category_inflows_cleaned.csv")
folio = pd.read_csv(f"{PROCESSED_PATH}/06_industry_folio_count_cleaned.csv")
performance = pd.read_csv(f"{PROCESSED_PATH}/07_scheme_performance_cleaned.csv")
transactions = pd.read_csv(f"{PROCESSED_PATH}/08_investor_transactions_cleaned.csv")
holdings = pd.read_csv(f"{PROCESSED_PATH}/09_portfolio_holdings_cleaned.csv")
benchmark = pd.read_csv(f"{PROCESSED_PATH}/10_benchmark_indices_cleaned.csv")

# ============================
# Prepare date dimension
# ============================
all_dates = pd.concat([
    pd.to_datetime(nav_history["date"], errors="coerce"),
    pd.to_datetime(aum["date"], errors="coerce"),
    pd.to_datetime(sip["month"], errors="coerce"),
    pd.to_datetime(category_inflows["month"], errors="coerce"),
    pd.to_datetime(folio["month"], errors="coerce"),
    pd.to_datetime(transactions["transaction_date"], errors="coerce"),
    pd.to_datetime(holdings["portfolio_date"], errors="coerce"),
    pd.to_datetime(benchmark["date"], errors="coerce")
]).dropna().drop_duplicates().sort_values()

dim_date = pd.DataFrame({"full_date": all_dates})
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.month_name()
dim_date["day"] = dim_date["full_date"].dt.day
dim_date["weekday_name"] = dim_date["full_date"].dt.day_name()

# ============================
# Rename columns for fact tables
# ============================
nav_fact = nav_history.rename(columns={"date": "nav_date"})
aum_fact = aum.rename(columns={"date": "aum_date"})

# performance columns to keep only fact columns
performance_fact = performance[
    [
        "amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
        "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
        "aum_crore", "expense_ratio_pct", "morningstar_rating", "risk_grade"
    ]
].copy()

# transactions columns to keep
transactions_fact = transactions[
    [
        "investor_id", "transaction_date", "amfi_code", "transaction_type",
        "amount_inr", "state", "city", "city_tier", "age_group",
        "gender", "annual_income_lakh", "payment_mode", "kyc_status"
    ]
].copy()

# ============================
# Load into SQLite
# ============================
fund_master.to_sql("dim_fund", engine, if_exists="replace", index=False)
dim_date.to_sql("dim_date", engine, if_exists="replace", index=False)
nav_fact.to_sql("fact_nav", engine, if_exists="replace", index=False)
transactions_fact.to_sql("fact_transactions", engine, if_exists="replace", index=False)
performance_fact.to_sql("fact_performance", engine, if_exists="replace", index=False)
aum_fact.to_sql("fact_aum", engine, if_exists="replace", index=False)

print("All cleaned datasets loaded into SQLite successfully.")

# ============================
# Verify row counts
# ============================
tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

with engine.connect() as conn:
    print("\nRow Counts in SQLite Database")
    print("-" * 40)
    for table in tables:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"{table}: {count}")